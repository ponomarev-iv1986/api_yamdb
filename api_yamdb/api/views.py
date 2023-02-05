from rest_framework.views import APIView
from rest_framework import status
from .serializers import (
    UserRegSerializer,
    TokenGetSerializer,
    UsersSerializer,
)
from rest_framework.response import Response
import uuid
from django.core.mail import send_mail
from users.models import User
from django.shortcuts import get_object_or_404
from rest_framework import viewsets
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework import permissions
from .permissions import (
    IsAdmin,
    IsUser,
)
from rest_framework import filters
from rest_framework.pagination import PageNumberPagination
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.decorators import action

# Create your views here.
class RegView(APIView):
    '''View для регистрации юзера и получение кода подтверждения'''

    permission_classes = (permissions.AllowAny,)

    def post(self, request):
        serializer = UserRegSerializer(data=request.data)
        if User.objects.filter(
            username=request.data.get('username'),
            email=request.data.get('email'),
        ).exists():
            return Response(request.data, status=status.HTTP_200_OK)
        if serializer.is_valid():
            username = serializer.validated_data.get('username')
            email = serializer.validated_data.get('email')
            confirmation_code = uuid.uuid4()
            send_mail(
                subject='Confirmation_code',
                message=f'Confirmation_code - {confirmation_code}',
                from_email=['test@test.io'],
                recipient_list=[email],
            )
            serializer.save()
            User.objects.filter(username=username).update(
                confirmation_code=confirmation_code, is_active=True
            )
            return Response(
                serializer.validated_data, status=status.HTTP_200_OK
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class TokenGetView(APIView):
    '''View для получения токена, эндпойнт'''

    permission_classes = (permissions.AllowAny,)

    def post(self, request):
        serializer = TokenGetSerializer(data=request.data)
        if serializer.is_valid():
            username = serializer.validated_data.get('username')
            user = get_object_or_404(User, username=username)
            confirmation_code = serializer.validated_data.get(
                'confirmation_code'
            )
            if user.confirmation_code == confirmation_code:
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
    '''Viewset для'''

    permission_classes = (IsAdmin,)
    queryset = User.objects.all()
    serializer_class = UsersSerializer
    pagination_class = PageNumberPagination
    filter_backends = (DjangoFilterBackend, filters.SearchFilter)
    search_fields = ('username',)
    lookup_field = 'username'
    http_method_names = ['get', 'post', 'patch', 'delete']

    @action(
        detail=False,
        methods=['get', 'patch'],
        url_path='me',
        permission_classes=(permissions.IsAuthenticated,),
    )
    def me(self, request):
        serializer = UsersSerializer(request.user)
        if request.method == 'PATCH':
            serializer = UsersSerializer(
                request.user, data=request.data, partial=True
            )
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.data, status=status.HTTP_200_OK)
