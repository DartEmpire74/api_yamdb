from django.db import models


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
        related_name='posts',
        blank=False,
        null=True,
    )

    class Meta:
        verbose_name = 'произведение'
        verbose_name_plural = 'Произведения'

    def __str__(self):
        return self.name
