from rest_framework import serializers
from users.models import User
from django.core.validators import RegexValidator
from rest_framework.validators import ValidationError


class UserRegSerializer(serializers.ModelSerializer):
    email = serializers.CharField(max_length=254, allow_blank=False)
    username = serializers.CharField(
        max_length=150,
        allow_blank=False,
        validators=[
            RegexValidator(
                regex=r'^[\w.@+-]+', message='Введите корректный username'
            )
        ],
    )

    class Meta:
        model = User
        fields = (
            'email',
            'username',
        )

    def validate_username(self, value):
        if value == 'me' or '':
            raise serializers.ValidationError(
                {'me нельзя использовать в качестве username'},
            )
        if User.objects.filter(username=value).exists():
            raise serializers.ValidationError(
                {'username уже существует'},
            )
        return value

    def validate_email(self, value):
        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError(
                {'email уже существует'},
            )
        return value


class TokenGetSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('username', 'confirmation_code')
