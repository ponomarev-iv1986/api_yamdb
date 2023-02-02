from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.permissions import AllowAny
from .serializers import UserRegSerializer, TokenGetSerializer
from rest_framework.response import Response
import uuid
from django.core.mail import send_mail
from users.models import User
from django.shortcuts import get_object_or_404
from rest_framework_simplejwt.tokens import RefreshToken

# Create your views here.
class RegView(APIView):
    permission_classes = (AllowAny,)

    def post(self, request):
        serializer = UserRegSerializer(data=request.data)
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
    permission_classes = (AllowAny,)

    def post(self, request):
        serializer = TokenGetSerializer(data=request.data)
        serializer.is_valid()
        username = serializer.data['username']
        user = get_object_or_404(User, username=username)
        confirmation_code = serializer.data['confirmation_code']
        if user.confirmation_code != confirmation_code:
            return Response(
                {'Не верный confirmation code'},
                status=status.HTTP_400_BAD_REQUEST,
            )
        token = RefreshToken.for_user(user)
        return Response(
            {'token': str(token.access_token)}, status=status.HTTP_200_OK
        )
