import uuid

from django.core.mail import send_mail
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, mixins, serializers, status, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import (AllowAny, IsAuthenticated,
                                        IsAuthenticatedOrReadOnly)
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from reviews.models import Category, Genre, Review, Title
from users.models import User

from .permissions import AdminOrSuperUser, IsAdminOrSuperuser, ReviewPermission
from .serializers import (CategorySerializer, CommentSerializer,
                          GenreSerializer, ReviewSerializer, SignUpSerializer,
                          TitleListRetrieveSerializer, TitleSerializer,
                          TokenGetSerializer, UsersSerializer)


class SignUpView(APIView):
    """
    Регистрация пользователя и получение кода подтверждения.
    """

    permission_classes = (AllowAny,)

    def post(self, request):
        serializer = SignUpSerializer(data=request.data)
        if User.objects.filter(
            username=request.data.get('username'),
            email=request.data.get('email'),
        ).exists():
            return Response(request.data, status=status.HTTP_200_OK)
        if serializer.is_valid():
            email = serializer.validated_data.get('email')
            confirmation_code = uuid.uuid4()
            send_mail(
                subject='Confirmation_code',
                message=f'Confirmation_code - {confirmation_code}',
                from_email=['test@test.io'],
                recipient_list=[email],
            )
            serializer.save()
            User.objects.filter(
                username=serializer.validated_data.get('username')
            ).update(confirmation_code=confirmation_code, is_active=True)
            return Response(
                serializer.validated_data, status=status.HTTP_200_OK
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class TokenGetView(APIView):
    """
    Получение токена.
    """

    permission_classes = (AllowAny,)

    def post(self, request):
        serializer = TokenGetSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = get_object_or_404(
            User, username=serializer.validated_data.get('username')
        )
        if user.confirmation_code == serializer.validated_data.get(
            'confirmation_code'
        ):
            token = RefreshToken.for_user(user)
            return Response(
                {'token': str(token.access_token)},
                status=status.HTTP_200_OK,
            )
        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST,
        )


class UsersViewSet(viewsets.ModelViewSet):
    """
    Получение, изменение информации о пользователях.
    """

    permission_classes = (AdminOrSuperUser,)
    queryset = User.objects.all()
    serializer_class = UsersSerializer
    filter_backends = (DjangoFilterBackend, filters.SearchFilter)
    search_fields = ('username',)
    lookup_field = 'username'
    http_method_names = ['get', 'post', 'patch', 'delete']

    @action(
        detail=False,
        methods=['get', 'patch'],
        url_path='me',
        permission_classes=(IsAuthenticated,),
    )
    def users_me(self, request):
        serializer = UsersSerializer(request.user)
        if request.method == 'PATCH':
            serializer = UsersSerializer(
                request.user, data=request.data, partial=True
            )
            serializer.is_valid(raise_exception=True)
            serializer.save(role=request.user.role, partial=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.data, status=status.HTTP_200_OK)


class CategoryViewSet(mixins.ListModelMixin, mixins.CreateModelMixin,
                      mixins.DestroyModelMixin, viewsets.GenericViewSet):
    """
    Получение, добавление, удаление категорий.
    """

    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    lookup_field = 'slug'
    permission_classes = (IsAdminOrSuperuser,)
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name',)

    def get_permissions(self):
        if self.action in ['list', 'retrieve']:
            return (IsAuthenticatedOrReadOnly(),)
        return super().get_permissions()


class GenreViewSet(mixins.ListModelMixin, mixins.CreateModelMixin,
                   mixins.DestroyModelMixin, viewsets.GenericViewSet):
    """
    Получение, добавление, удаление жанров.
    """

    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    lookup_field = 'slug'
    permission_classes = (IsAdminOrSuperuser,)
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name',)

    def get_permissions(self):
        if self.action in ['list', 'retrieve']:
            return (IsAuthenticatedOrReadOnly(),)
        return super().get_permissions()


class TitleViewSet(viewsets.ModelViewSet):
    """
    Получение, добавление, изменение, удаление произведений.
    """

    permission_classes = (IsAdminOrSuperuser,)

    def get_queryset(self):
        queryset = Title.objects.all()
        category = self.request.query_params.get('category')
        genre = self.request.query_params.get('genre')
        name = self.request.query_params.get('name')
        year = self.request.query_params.get('year')
        if category is not None:
            return queryset.filter(category__slug=category)
        if genre is not None:
            return queryset.filter(genre__slug=genre)
        if year is not None:
            return queryset.filter(year=year)
        if name is not None:
            return queryset.filter(name=name)
        return queryset

    def get_permissions(self):
        if self.action in ['list', 'retrieve']:
            return (IsAuthenticatedOrReadOnly(),)
        return super().get_permissions()

    def get_serializer_class(self):
        if self.action in ['list', 'retrieve']:
            return TitleListRetrieveSerializer
        return TitleSerializer


class ReviewViewSet(viewsets.ModelViewSet):
    """
    Получение, добавление, изменение, удаление отзывов.
    """

    serializer_class = ReviewSerializer
    permission_classes = (ReviewPermission,)

    def get_queryset(self):
        title = get_object_or_404(Title, id=self.kwargs['title_id'])
        return title.reviews.all()

    def perform_create(self, serializer):
        title = get_object_or_404(Title, id=self.kwargs['title_id'])
        if Review.objects.filter(
                author=self.request.user, title=title).exists():
            raise serializers.ValidationError(
                'Ваш отзыв на это произведение уже существует'
            )
        serializer.save(author=self.request.user, title=title)


class CommentViewSet(viewsets.ModelViewSet):
    """
    Получение, добавление, изменение, удаление произведений.
    """

    serializer_class = CommentSerializer
    permission_classes = (ReviewPermission,)

    def get_queryset(self):
        review = get_object_or_404(Review, id=self.kwargs['review_id'])
        return review.comments.all()

    def perform_create(self, serializer):
        review = get_object_or_404(
            Review, id=self.kwargs['review_id'],
            title=self.kwargs['title_id']
        )
        serializer.save(author=self.request.user, review=review)
