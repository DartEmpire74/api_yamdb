import datetime as dt

from django.db.models import Avg
from rest_framework import serializers
from rest_framework.relations import (
    SlugRelatedField)

from reviews.models import (
    Comment, Review, Category, Genre, Title)


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
        return average_rating if average_rating is not None else 0


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
