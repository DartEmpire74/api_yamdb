from django.contrib.auth.models import AbstractUser
from django.db import models

from .constants import EMAIL_MAX_LENGTH, ROLE_MAX_LENGTH, USER_MAX_LENGTH

from .validators import validate_username


class User(AbstractUser):
    """Модель пользователя."""

    USER = 'user'
    ADMIN = 'admin'
    MODERATOR = 'moderator'

    CHOICES = (
        (USER, 'Аутентифицированный пользователь'),
        (ADMIN, 'Администратор'),
        (MODERATOR, 'Модератор')
    )
    username = models.CharField(verbose_name='Пользователь',
                                validators=(validate_username,),
                                max_length=USER_MAX_LENGTH,
                                unique=True)
    first_name = models.CharField(verbose_name='Имя',
                                  max_length=USER_MAX_LENGTH,
                                  blank=True)
    last_name = models.CharField(verbose_name='Фамилия',
                                 max_length=USER_MAX_LENGTH,
                                 blank=True)
    email = models.EmailField(verbose_name='Электронная почта',
                              max_length=EMAIL_MAX_LENGTH,
                              unique=True)
    bio = models.TextField(verbose_name='Биография',
                           blank=True)
    role = models.CharField(verbose_name='Пользовательская роль',
                            max_length=ROLE_MAX_LENGTH,
                            choices=CHOICES,
                            default=USER)

    class Meta:
        ordering = ('id',)
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

    def __str__(self):
        return self.username

    @property
    def is_admin(self):
        return self.role == User.ADMIN or self.is_superuser

    @property
    def is_moderator(self):
        return self.role == User.MODERATOR
