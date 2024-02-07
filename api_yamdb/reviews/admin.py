from django.contrib import admin
from django.db.models import Avg

from .models import (
    Category, Comment, Genre, Review, Title)


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug')
    search_fields = ('name', 'slug')
    list_filter = ('name',)


@admin.register(Genre)
class GenreAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug')
    search_fields = ('name', 'slug')
    list_filter = ('name',)


@admin.register(Title)
class TitleAdmin(admin.ModelAdmin):
    list_display = (
        'name', 'description', 'year', 'get_average_score', 'display_genres',
        'category')
    search_fields = ('name', 'description')
    list_filter = ['year']
    list_editable = ['category']

    @admin.display(description='Рейтинг')
    def get_average_score(self, obj):
        average_score = obj.reviews.aggregate(Avg('score'))['score__avg']
        return round(average_score, 2) if average_score else None

    @admin.display(description='Жанры')
    def display_genres(self, obj):
        return ', '.join([genre.name for genre in obj.genre.all()])


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ('author', 'text', 'pub_date', 'score')
    search_fields = ('author__username', 'text')
    list_filter = ('pub_date', 'score')


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('author', 'text', 'pub_date', 'review')
    search_fields = ('author__username', 'text')
    list_filter = ('pub_date',)
