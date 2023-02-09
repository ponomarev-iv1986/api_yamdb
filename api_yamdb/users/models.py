from django.contrib.auth.models import AbstractUser
from django.db import models
from .userroles import UserRoles


class User(AbstractUser):
    """Пользователи."""

    first_name = models.CharField(
        max_length=150, verbose_name='Имя', blank=True
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
        choices=UserRoles,
        default=UserRoles.USER,
    )
    confirmation_code = models.CharField(
        max_length=50, blank=True, verbose_name='Проверочный код'
    )

    @property
    def is_user(self):
        if self.role == UserRoles.USER:
            return True

    @property
    def is_moderator(self):
        if self.role == UserRoles.MODERATOR:
            return True

    @property
    def is_admin(self):
        if self.role == UserRoles.ADMIN:
            return True
