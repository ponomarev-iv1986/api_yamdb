from django.core.exceptions import ValidationError
from users.models import User


def validate_email(value):
    if User.objects.filter(email=value).exists():
        raise ValidationError(
            {'email уже существует'},
        )
    return value


def validate_username(value):
    if value == 'me':
        raise ValidationError(
            {'me нельзя использовать в качестве username'},
        )
    return value
