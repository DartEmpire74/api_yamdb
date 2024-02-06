from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.contrib.auth import get_user_model


User = get_user_model()


MAX_CHARS_LENGTH = 256
MAX_SLUG_LENGTH = 50


class BaseModelsMixin(models.Model):
    name = models.CharField(
        verbose_name='Название',
        max_length=MAX_CHARS_LENGTH,
        blank=False,
    )
    slug = models.SlugField(
        verbose_name='Слаг',
        max_length=MAX_SLUG_LENGTH,
        unique=True,
        blank=False,
    )

    class Meta:
        abstract = True

    def __str__(self):
        return self.name


class Category(BaseModelsMixin):

    class Meta:
        verbose_name = 'категория'
        verbose_name_plural = 'Категории'


class Genre(BaseModelsMixin):

    class Meta:
        verbose_name = 'жанр'
        verbose_name_plural = 'Жанры'


class Title(models.Model):
    name = models.CharField(
        verbose_name='Название',
        max_length=MAX_CHARS_LENGTH,
        blank=False,
    )
    year = models.IntegerField(
        verbose_name='Год выпуска',
        blank=False,
    )
    description = models.TextField(
        verbose_name='Описание',
        blank=True,
    )
    genre = models.ManyToManyField(
        'Genre',
        verbose_name='Жанры',
        related_name='titles',
        blank=False,
    )
    category = models.ForeignKey(
        'Category',
        models.SET_NULL,
        verbose_name='Категории',
        related_name='posts',
        blank=False,
        null=True,
    )

    class Meta:
        ordering = ('-year', )
        verbose_name = 'произведение'
        verbose_name_plural = 'Произведения'

    def __str__(self):
        return self.name


class Review(models.Model):
    text = models.TextField(verbose_name='Текст')
    author = models.ForeignKey(
        User,
        verbose_name='Автор',
        on_delete=models.CASCADE,
        related_name='reviews'
    )
    pub_date = models.DateTimeField(
        'Дата добавления', auto_now_add=True, db_index=True)
    score = models.IntegerField(
        'Оценка', validators=[MinValueValidator(1), MaxValueValidator(10)]
    )
    title = models.ForeignKey(
        Title,
        on_delete=models.CASCADE,
        related_name='reviews',
    )

    class Meta:
        verbose_name = 'отзыв'
        verbose_name_plural = 'Отзывы'
        constraints = [
            models.UniqueConstraint(
                fields=['author', 'title'],
                name='unique_author_title_review')
        ]

    def __str__(self):
        return self.text


class Comment(models.Model):
    author = models.ForeignKey(
        User,
        verbose_name='Автор',
        on_delete=models.CASCADE,
        related_name='comments'
    )
    text = models.TextField(verbose_name='Текст')
    pub_date = models.DateTimeField(
        'Дата добавления', auto_now_add=True, db_index=True)
    review = models.ForeignKey(
        Review, on_delete=models.CASCADE, related_name='comments')

    class Meta:

        verbose_name = 'комментарий'
        verbose_name_plural = 'Комментарии'
