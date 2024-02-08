from django.contrib.auth import get_user_model
from django.db import models

from reviews.constants import (
    MAX_CHARS_LENGTH, MAX_TEXT_LENGTH, MAX_VALUE_VALIDATOR,
    MIN_VALUE_VALIDATOR)
from reviews.validators import validate_year


User = get_user_model()


class AuthorTextDateMixin(models.Model):
    author = models.ForeignKey(
        User,
        verbose_name='Автор',
        on_delete=models.CASCADE)
    text = models.TextField(verbose_name='Текст')
    pub_date = models.DateTimeField(
        'Дата добавления', auto_now_add=True, db_index=True)

    class Meta:
        abstract = True
        ordering = ('-pub_date',)

    def __str__(self):
        if len(self.text) > MAX_TEXT_LENGTH:
            return self.text[:MAX_TEXT_LENGTH] + '...'
        return self.text


class NameSlugMixin(models.Model):
    name = models.CharField(
        verbose_name='Название',
        max_length=MAX_CHARS_LENGTH
    )
    slug = models.SlugField(
        verbose_name='Слаг',
        unique=True,
    )

    class Meta:
        abstract = True
        ordering = ('name',)

    def __str__(self):
        return self.name


class Category(NameSlugMixin):

    class Meta(NameSlugMixin.Meta):
        verbose_name = 'категория'
        verbose_name_plural = 'Категории'


class Genre(NameSlugMixin):

    class Meta(NameSlugMixin.Meta):
        verbose_name = 'жанр'
        verbose_name_plural = 'Жанры'


class Title(models.Model):
    name = models.CharField(
        verbose_name='Название',
        max_length=MAX_CHARS_LENGTH,
    )
    year = models.SmallIntegerField(
        verbose_name='Год выпуска',
        validators=[validate_year],
    )
    description = models.TextField(
        verbose_name='Описание',
        blank=True,
    )
    genre = models.ManyToManyField(
        'Genre',
        verbose_name='Жанры',
        related_name='titles'
    )
    category = models.ForeignKey(
        'Category',
        models.SET_NULL,
        verbose_name='Категории',
        null=True,
        related_name='titles'
    )

    class Meta:
        ordering = ('-year', )
        verbose_name = 'произведение'
        verbose_name_plural = 'Произведения'

    def __str__(self):
        return self.name


class Review(AuthorTextDateMixin):
    score = models.PositiveSmallIntegerField(
        'Оценка', validators=[MIN_VALUE_VALIDATOR, MAX_VALUE_VALIDATOR])
    title = models.ForeignKey(
        Title,
        verbose_name='Произведение',
        on_delete=models.CASCADE)

    class Meta(AuthorTextDateMixin.Meta):
        default_related_name = 'reviews'
        verbose_name = 'отзыв'
        verbose_name_plural = 'Отзывы'
        constraints = [
            models.UniqueConstraint(
                fields=['author', 'title'],
                name='unique_author_title_review')]


class Comment(AuthorTextDateMixin):
    review = models.ForeignKey(
        Review, verbose_name='Отзыв',
        on_delete=models.CASCADE)

    class Meta(AuthorTextDateMixin.Meta):
        default_related_name = 'comments'
        verbose_name = 'комментарий'
        verbose_name_plural = 'Комментарии'
