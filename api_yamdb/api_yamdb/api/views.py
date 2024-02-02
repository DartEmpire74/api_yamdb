from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from django.db import IntegrityError
from django.shortcuts import get_object_or_404
from rest_framework import filters
from rest_framework import status
from rest_framework.decorators import action, api_view, permission_classes
from rest_framework.exceptions import ValidationError
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from rest_framework_simplejwt.tokens import AccessToken


from .permissions import (
    IsAdmin,
    # IsAdminOrReadOnly,
    # IsAuthorModeratorAdminOrReadOnly
)
from .serializers import (
    CustomUserSerializer,
    ProfileEditSerializer,
    SignUpSerializer,
    TokenSerializer,
)
from api_yamdb.settings import DEFAULT_FROM_EMAIL
from users.models import User


class UserViewSet(ModelViewSet):
    """Управление данными пользователя."""
    queryset = User.objects.all()
    serializer_class = CustomUserSerializer
    permission_classes = (IsAdmin, )
    lookup_field = 'username'
    filter_backends = (filters.SearchFilter, )
    search_fields = ('username', )
    http_method_names = ['get', 'post', 'patch', 'delete']

    @action(methods=['GET', 'PATCH'], detail=False,
            permission_classes=(IsAuthenticated, ))
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
        user, _ = User.objects.get_or_create(username=request.data['username'],
                                             email=request.data['email'])
    except IntegrityError:
        raise ValidationError('Неверное сочетание имени пользователя и email')
    confirmation_code = default_token_generator.make_token(user)
    send_mail('Подтверждение регистрации на сайте Yamdb!',
              f'Ваш код: {confirmation_code} для подтверждения регистрации',
              DEFAULT_FROM_EMAIL,
              [user.email],
              fail_silently=False)
    return Response({'email': user.email,
                     'username': user.username},
                    status=status.HTTP_200_OK)


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
