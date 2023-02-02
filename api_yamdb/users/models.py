from django.db import models

# Create your models here.
from django.contrib.auth.models import AbstractUser


ADMIN = 'admin'
MODERATOR = 'moderator'
USER = 'user'

USER_ROLE = (
    (USER, 'user'),
    (MODERATOR, 'moderator'),
    (ADMIN, 'admin'),
)


class User(AbstractUser):

    username = models.CharField(
        max_length=150,
        verbose_name='Логин',
        unique=True,
    )
    email = models.EmailField(
        max_length=254,
        verbose_name='Email',
        unique=True,
        blank=False,
    )

    first_name = models.CharField(
        max_length=150, verbose_name='Имя', help_text='Имя', blank=True
    )
    last_name = models.CharField(
        max_length=150,
        verbose_name='Фамилия',
        blank=True,
    )
    bio = models.TextField(
        max_length=1000,
        verbose_name='Биография',
        blank=True,
    )
    role = models.CharField(
        max_length=100,
        verbose_name='Роль',
        choices=USER_ROLE,
        default=USER,
    )
    confirmation_code = models.CharField(
        max_length=50, blank=True, verbose_name='Проверочный код'
    )

    def __str__(self):
        return self.username
