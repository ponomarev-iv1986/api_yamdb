from django.core.validators import RegexValidator
from rest_framework import serializers
from reviews.models import Category, Comment, Genre, Review, Title
from users.models import User


class SignUpSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(max_length=254, allow_blank=False)
    username = serializers.CharField(
        max_length=150,
        allow_blank=False,
        validators=[
            RegexValidator(
                regex=r'^[\w.@+-]+\Z', message='Введите корректный username'
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
        if value == 'me':
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
    username = serializers.CharField(required=True)
    confirmation_code = serializers.CharField(required=True)

    class Meta:
        model = User
        fields = ('username', 'confirmation_code')


class UsersSerializer(serializers.ModelSerializer):
    username = serializers.CharField(
        max_length=150,
        allow_blank=False,
        validators=[
            RegexValidator(
                regex=r'^[\w.@+-]+\Z', message='Введите корректный username'
            )
        ],
        required=True,
    )
    email = serializers.EmailField(
        max_length=254, required=True, allow_blank=False
    )

    class Meta:
        model = User
        fields = (
            'username',
            'email',
            'first_name',
            'last_name',
            'bio',
            'role',
        )
        read_only_field = ('role',)

    def validate_username(self, value):
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


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ('name', 'slug')


class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Genre
        fields = ('name', 'slug')


class TitleSerializer(serializers.ModelSerializer):
    genre = serializers.SlugRelatedField(
        many=True, slug_field='slug', queryset=Genre.objects.all()
    )
    category = serializers.SlugRelatedField(
        slug_field='slug', queryset=Category.objects.all()
    )

    class Meta:
        model = Title
        fields = ('id', 'name', 'year', 'description', 'genre', 'category')


class TitleListRetrieveSerializer(serializers.ModelSerializer):
    rating = serializers.SerializerMethodField()
    genre = GenreSerializer(read_only=True, many=True)
    category = CategorySerializer(read_only=True)

    class Meta:
        model = Title
        fields = (
            'id',
            'name',
            'year',
            'rating',
            'description',
            'genre',
            'category',
        )

    def get_rating(self, obj):
        reviews = obj.reviews.all()
        scores = []
        for review in reviews:
            scores.append(review.score)
        if scores:
            return int(sum(scores) / len(scores))
        return None


class ReviewSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        read_only=True, slug_field='username'
    )

    class Meta:
        model = Review
        fields = ('id', 'text', 'author', 'score', 'pub_date')
        read_only_fields = ('pub_date',)


class CommentSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        read_only=True, slug_field='username'
    )

    class Meta:
        model = Comment
        fields = ('id', 'text', 'author', 'pub_date')
        read_only_fields = ('pub_date',)
