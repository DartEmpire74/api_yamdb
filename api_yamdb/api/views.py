from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from django.db import IntegrityError
from django.db.models import Avg
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import status, viewsets
from rest_framework.decorators import action, api_view, permission_classes
from rest_framework.exceptions import ValidationError
from rest_framework.filters import SearchFilter
from rest_framework.permissions import (
    AllowAny, IsAuthenticated, IsAuthenticatedOrReadOnly)
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import AccessToken

from api.filters import TitleFilter
from api.mixins import ListCreateDestroyViewSet, PatchOnlyMixin
from api.permissions import IsAdmin, IsAdminOrReadOnly, IsAuthorModeratorAdmin
from api.serializers import (
    CategorySerializer, CommentSerializer, GenreSerializer,
    ReviewSerializer, SignUpSerializer, TitleSerializer,
    TokenSerializer, UserSerializer)
from reviews.models import Category, Genre, Review, Title


User = get_user_model()


class CategoryViewSet(ListCreateDestroyViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class GenreViewSet(ListCreateDestroyViewSet):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer


class TitleViewSet(PatchOnlyMixin, viewsets.ModelViewSet):
    queryset = Title.objects.annotate(
        rating=Avg('reviews__score')).all()
    serializer_class = TitleSerializer
    permission_classes = (IsAdminOrReadOnly,)
    filter_backends = (DjangoFilterBackend,)
    filterset_class = TitleFilter


class ReviewViewSet(PatchOnlyMixin, viewsets.ModelViewSet):
    serializer_class = ReviewSerializer
    permission_classes = (
        IsAuthenticatedOrReadOnly,
        IsAuthorModeratorAdmin
    )

    def get_title_model(self):
        title_id = self.kwargs.get('title_id')
        return get_object_or_404(Title, id=title_id)

    def perform_create(self, serializer):
        title = self.get_title_model()
        serializer.save(author=self.request.user, title=title)

    def get_queryset(self):
        title = self.get_title_model()
        return title.reviews.all()


class CommentViewSet(PatchOnlyMixin, viewsets.ModelViewSet):
    serializer_class = CommentSerializer
    permission_classes = (
        IsAuthenticatedOrReadOnly,
        IsAuthorModeratorAdmin
    )

    def get_review_model(self):
        review_id = self.kwargs.get('review_id')
        return get_object_or_404(Review, id=review_id)

    def perform_create(self, serializer):
        review = self.get_review_model()
        serializer.save(author=self.request.user, review=review)

    def get_queryset(self):
        review = self.get_review_model()
        return review.comments.all()


class UserViewSet(PatchOnlyMixin, viewsets.ModelViewSet):
    """Управление данными пользователя."""

    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (IsAdmin,)
    lookup_field = 'username'
    filter_backends = (SearchFilter,)
    search_fields = ('username',)

    @action(
        methods=['GET', 'PATCH'],
        detail=False,
        permission_classes=(IsAuthenticated,)
    )
    def me(self, request):
        if request.method == 'PATCH':
            serializer = UserSerializer(
                request.user,
                data=request.data,
                partial=True
            )

            serializer.is_valid(raise_exception=True)
            serializer.save(role=request.user.role)

        serializer = UserSerializer(request.user)

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
        serializer.data,
        status=status.HTTP_200_OK
    )


@api_view(['POST'])
@permission_classes([AllowAny])
def token(request):
    """Получение токена."""
    serializer = TokenSerializer(data=request.data)

    serializer.is_valid(raise_exception=True)
    user = get_object_or_404(User, username=request.data['username'])
    token = AccessToken.for_user(user)
    respone = {'token': str(token)}

    return Response(respone, status=status.HTTP_200_OK)
