from django.urls import include, path
from .views import RegView, TokenGetView

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
]
