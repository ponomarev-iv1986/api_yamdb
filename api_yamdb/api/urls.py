from django.urls import include, path
from .views import RegView, TokenGetView, UsersViewSet, UserMeViewSet
from rest_framework.routers import DefaultRouter

router = DefaultRouter()


router.register('users', UsersViewSet, basename='users')
router.register(r'users/(?P<username>\d+)', UsersViewSet, basename='users')
router.register('users/me', UserMeViewSet, basename='usersme')

urlpatterns = [
    path(
        'v1/auth/signup/',
        RegView.as_view(),
        name='signup',
    ),
    path(
        'v1/auth/token/',
        TokenGetView.as_view(),
        name='tokenget',
    ),
    path('v1/', include(router.urls)),
]
