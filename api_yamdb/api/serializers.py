import datetime as dt

from django.contrib.auth import get_user_model
from django.contrib.auth.tokens import default_token_generator
from django.shortcuts import get_object_or_404

from rest_framework import serializers
from rest_framework.relations import SlugRelatedField
from rest_framework.validators import ValidationError

from reviews.models import Category, Comment, Genre, Review, Title
from users.validators import validate_username
from .constants import EMAIL_MAX_LENGTH, USER_MAX_LENGTH
from .utils import get_title_model


User = get_user_model()


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
        slug_field='slug',
        queryset=Genre.objects.all(),
        many=True,
        required=True,
        allow_empty=False,
    )
    rating = serializers.FloatField(source='avg_rating', read_only=True)

    class Meta:
        model = Title
        fields = '__all__'

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


class CommentSerializer(serializers.ModelSerializer):

    author = SlugRelatedField(slug_field='username', read_only=True)

    class Meta:
        fields = ('id', 'text', 'author', 'pub_date')
        model = Comment


class ReviewSerializer(serializers.ModelSerializer):

    author = SlugRelatedField(
        slug_field='username', read_only=True)

    class Meta:
        fields = ('id', 'text', 'author', 'pub_date', 'score')
        model = Review

    def validate(self, data):
        if self.context['request'].method == 'POST':
            title = get_title_model(
                self.context['view'].kwargs.get('title_id')
            )
            author = self.context['request'].user
            existing_review = Review.objects.filter(
                author=author,
                title=title
            ).exists()

            if existing_review:
                raise serializers.ValidationError(
                    "Вы уже оставили отзыв на это произведение."
                )

        return data


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


class UserSerializer(serializers.ModelSerializer):
    """Serializer для модели пользователя."""

    class Meta:
        fields = ('username', 'email', 'first_name',
                  'last_name', 'bio', 'role', )
        model = User
