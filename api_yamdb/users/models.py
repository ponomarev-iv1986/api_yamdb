from django.contrib.auth.models import AbstractUser
from django.db import models

from .userroles import UserRoles


class User(AbstractUser):
    """Пользователи."""

    bio = models.TextField(
        max_length=1000,
        verbose_name='Биография',
        blank=True,
    )
    role = models.CharField(
        max_length=100,
        verbose_name='Роль',
        choices=UserRoles.choices,
        default=UserRoles.USER,
    )
    confirmation_code = models.CharField(
        max_length=50, blank=True, verbose_name='Проверочный код'
    )

    @property
    def is_user(self):
        return self.role == UserRoles.USER

    @property
    def is_moderator(self):
        return self.role == UserRoles.MODERATOR

    @property
    def is_admin(self):
        return self.role == UserRoles.ADMIN
