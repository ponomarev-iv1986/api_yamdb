from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import (CategoryViewSet, CommentViewSet, GenreViewSet,
                    ReviewViewSet, SignUpView, TitleViewSet, TokenGetView,
                    UsersViewSet)

router = DefaultRouter()

router.register('users', UsersViewSet, basename='users')
router.register('categories', CategoryViewSet)
router.register('genres', GenreViewSet)
router.register('titles', TitleViewSet, basename='titles')
router.register(
    r'titles/(?P<title_id>\d+)/reviews', ReviewViewSet, basename='reviews'
)
router.register(
    r'titles/(?P<title_id>\d+)/reviews/(?P<review_id>\d+)/comments',
    CommentViewSet,
    basename='comments',
)

urlpatterns = [
    path(
        'auth/signup/',
        SignUpView.as_view(),
        name='signup',
    ),
    path(
        'auth/token/',
        TokenGetView.as_view(),
        name='token',
    ),
    path('', include(router.urls)),
]
