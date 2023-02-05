from django.urls import include, path
from .views import RegView, TokenGetView, UsersViewSet  # UserMeViewSet
from rest_framework.routers import DefaultRouter
from .views import (CategoryViewSet,
                    GenreViewSet,
                    TitleViewSet,
                    ReviewViewSet,
                    CommentViewSet)

router = DefaultRouter()


router.register('users', UsersViewSet, basename='users')
router.register('categories', CategoryViewSet)
router.register('genres', GenreViewSet)
router.register('titles', TitleViewSet)
router.register(r'titles/(?P<title_id>\d+)/reviews',
                ReviewViewSet, basename='reviews')
router.register(
    r'titles/(?P<title_id>\d+)/reviews/(?P<review_id>\d+)/comments',
    CommentViewSet,
    basename='comments'
)

urlpatterns = [
    path(
        'v1/auth/signup/',
        RegView.as_view(),
        name='signup',
    ),
    path(
        'v1/auth/token/',
        TokenGetView.as_view(),
        name='token',
    ),
    path('v1/', include(router.urls)),
]
