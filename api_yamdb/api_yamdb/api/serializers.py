from django.contrib.auth.tokens import default_token_generator
from django.shortcuts import get_object_or_404
from rest_framework import serializers
from rest_framework.validators import ValidationError

from .constants import EMAIL_MAX_LENGTH, USER_MAX_LENGTH
from users.models import User
from users.validators import validate_username


class SignUpSerializer(serializers.Serializer):
    """Serializer для регистрации пользователя."""

    username = serializers.CharField(max_length=USER_MAX_LENGTH,
                                     required=True,
                                     validators=(validate_username,))
    email = serializers.EmailField(max_length=EMAIL_MAX_LENGTH,
                                   required=True)


class TokenSerializer(serializers.Serializer):
    """Serializer для получения токена."""

    username = serializers.CharField(max_length=USER_MAX_LENGTH,
                                     required=True,
                                     validators=(validate_username,))
    confirmation_code = serializers.CharField(required=True)

    def validate(self, data):
        user = get_object_or_404(User, username=data['username'])
        confirmation_code = data['confirmation_code']
        if not default_token_generator.check_token(user, confirmation_code):
            raise ValidationError('Введен неверный код подтверждения!')
        return data


class CustomUserSerializer(serializers.ModelSerializer):
    """Serializer для модели пользователя."""

    class Meta:
        fields = ('username', 'email', 'first_name',
                  'last_name', 'bio', 'role', )
        model = User


class ProfileEditSerializer(CustomUserSerializer):
    """Serializer для редактирования данных пользователя."""
    role = serializers.CharField(read_only=True)
