from django.conf import settings
from django.db import IntegrityError
from django.core.mail import send_mail
from django.contrib.auth import get_user_model
from django.contrib.auth.tokens import default_token_generator
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import status
from rest_framework.response import Response
from rest_framework.filters import SearchFilter
from rest_framework.exceptions import ValidationError
from rest_framework import viewsets
from rest_framework_simplejwt.tokens import AccessToken
from rest_framework.decorators import action, api_view, permission_classes
from rest_framework.permissions import (
    IsAuthenticatedOrReadOnly,
    AllowAny,
    IsAuthenticated,
)

from reviews.models import (
    Review,
    Comment,
    Category,
    Genre,
    Title
)
from .mixins import ListCreateDestroyViewSet, PatchOnlyMixin
from .filters import TitleFilter
from .permissions import (
    IsAuthorOrStaffOrReadOnly,
    IsAdmin,
    IsAdminOrReadOnly,
)
from .serializers import (
    CommentSerializer,
    ReviewSerializer,

    CategorySerializer,
    GenreSerializer,
    TitleSerializer,

    CustomUserSerializer,
    ProfileEditSerializer,
    SignUpSerializer,
    TokenSerializer,
)


User = get_user_model()


class CategoryViewSet(ListCreateDestroyViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = (IsAdminOrReadOnly, )
    lookup_field = 'slug'


class GenreViewSet(ListCreateDestroyViewSet):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    permission_classes = (IsAdminOrReadOnly, )
    lookup_field = 'slug'


class TitleViewSet(PatchOnlyMixin, viewsets.ModelViewSet):
    queryset = Title.objects.all()
    serializer_class = TitleSerializer
    permission_classes = (IsAdminOrReadOnly, )
    filter_backends = (DjangoFilterBackend, )
    filterset_class = TitleFilter


class ReviewViewSet(viewsets.ModelViewSet):
    serializer_class = ReviewSerializer
    permission_classes = (IsAuthenticated, )

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    def get_queryset(self):
        title = get_object_or_404(Title, id=self.kwargs['title_id'])
        return Review.objects.filter(title_id=title.id)


class CommentViewSet(viewsets.ModelViewSet):

    serializer_class = CommentSerializer
    permission_classes = (
        IsAuthenticatedOrReadOnly, IsAuthorOrStaffOrReadOnly)

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    def get_queryset(self):
        review = get_object_or_404(Review, id=self.kwargs['review_id'])
        return Comment.objects.filter(review_id=review.id)


class UserViewSet(PatchOnlyMixin, viewsets.ModelViewSet):
    """Управление данными пользователя."""
    queryset = User.objects.all()
    serializer_class = CustomUserSerializer
    permission_classes = (IsAdmin, )
    lookup_field = 'username'
    filter_backends = (SearchFilter, )
    search_fields = ('username', )

    @action(
        methods=['GET', 'PATCH'],
        detail=False,
        permission_classes=(IsAuthenticated, )
    )
    def me(self, request):
        user = get_object_or_404(User, username=self.request.user.username)
        if request.method == 'PATCH':
            serializer = ProfileEditSerializer(request.user,
                                               data=request.data,
                                               partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            return Response(serializer.errors,
                            status=status.HTTP_400_BAD_REQUEST)
        serializer = CustomUserSerializer(user)
        return Response(serializer.data)


@api_view(['POST'])
@permission_classes([AllowAny])
def signup(request):
    """Регистрация нового пользователя и отправка кода подтверждения."""
    serializer = SignUpSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)

    try:
        user, _ = User.objects.get_or_create(
            username=request.data['username'],
            email=request.data['email']
        )

    except IntegrityError:
        raise ValidationError(
            'Неверное сочетание имени пользователя и email'
        )

    confirmation_code = default_token_generator.make_token(user)

    send_mail(
        'Подтверждение регистрации на сайте Yamdb!',
        f'Ваш код: {confirmation_code} для подтверждения регистрации',
        settings.DEFAULT_FROM_EMAIL,
        [user.email],
        fail_silently=False
    )

    return Response(
        {
            'email': user.email,
            'username': user.username
        },
        status=status.HTTP_200_OK
    )


@api_view(['POST'])
@permission_classes([AllowAny])
def token(request):
    """Получение токена."""
    serializer = TokenSerializer(data=request.data)

    serializer.is_valid(raise_exception=True)
    user = get_object_or_404(User, username=request.data['username'])

    confirmation_code = request.data['confirmation_code']

    if default_token_generator.check_token(user, confirmation_code):
        token = AccessToken.for_user(user)
        respone = {'token': str(token)}

        return Response(respone, status=status.HTTP_200_OK)

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
