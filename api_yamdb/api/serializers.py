import datetime as dt

from django.contrib.auth import get_user_model
from django.contrib.auth.tokens import default_token_generator
from django.shortcuts import get_object_or_404
from django.db.models import Avg
from rest_framework import serializers
from rest_framework.validators import ValidationError
from rest_framework.relations import (
    SlugRelatedField)

from reviews.models import (
    Comment, Review, Category, Genre, Title)
from users.validators import validate_username


USER_MAX_LENGTH = 150
EMAIL_MAX_LENGTH = 254

User = get_user_model()


class CustomRelationField(serializers.RelatedField):

    def to_representation(self, value):
        return {
            'name': value.name,
            'slug': value.slug,
        }


class CategorySerializer(serializers.ModelSerializer):

    class Meta:
        model = Category
        exclude = ('id', )


class GenreSerializer(serializers.ModelSerializer):

    class Meta:
        model = Genre
        exclude = ('id', )


class TitleSerializer(serializers.ModelSerializer):
    category = serializers.SlugRelatedField(
        slug_field='slug', queryset=Category.objects.all()
    )
    genre = serializers.SlugRelatedField(
        slug_field='slug', queryset=Genre.objects.all(), many=True
    )
    rating = serializers.SerializerMethodField()

    class Meta:
        model = Title
        exclude = ()

    def to_representation(self, instance):
        rep = super().to_representation(instance)

        rep['genre'] = GenreSerializer(instance.genre.all(), many=True).data
        rep['category'] = CategorySerializer(instance.category).data

        return rep

    def validate_year(self, value):
        today_year = dt.date.today().year

        if value > today_year:
            raise serializers.ValidationError(
                'Год произведения не может быть больше текущего'
            )

        return value

    def get_rating(self, obj):
        reviews = Review.objects.filter(title=obj)
        average_rating = reviews.aggregate(Avg('score'))['score__avg']
        return average_rating if average_rating is not None else None


class CommentSerializer(serializers.ModelSerializer):

    author = SlugRelatedField(slug_field='username', read_only=True)

    class Meta:
        fields = ('id', 'text', 'author', 'pub_date')
        model = Comment


class ReviewSerializer(serializers.ModelSerializer):

    author = SlugRelatedField(slug_field='username', read_only=True)

    class Meta:
        fields = ('id', 'text', 'author', 'pub_date', 'score')
        model = Review


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
