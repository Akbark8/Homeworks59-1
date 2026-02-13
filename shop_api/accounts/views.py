import random
import string

from django.db import transaction


from rest_framework.views import APIView
from rest_framework.generics import CreateAPIView
from rest_framework.response import Response
from rest_framework import status

from .models import CustomUser, ConfirmationCode
from .serializers import (
    RegisterValidateSerializer,
    AuthValidateSerializer,
    ConfirmationSerializer,
    GoogleAuthSerializer,
)
from .tokens import CustomRefreshToken
from .confirmation_code_store import save_confirmation_code, consume_confirmation_code


class RegistrationAPIView(CreateAPIView):
    serializer_class = RegisterValidateSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)

        with transaction.atomic():
            user = CustomUser.objects.create_user(
                email=serializer.validated_data['email'],
                password=serializer.validated_data['password'],
                is_active=False
            )

            code = ''.join(random.choices(string.digits, k=6))

        save_confirmation_code(user.id, code)

        return Response(
            {
                'user_id': user.id,
                'confirmation_code': code
            },
            status=status.HTTP_201_CREATED
        )


class ConfirmUserAPIView(CreateAPIView):
    serializer_class = ConfirmationSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)

        user_id = serializer.validated_data['user_id']
        code = serializer.validated_data['code']

        with transaction.atomic():
            user = CustomUser.objects.get(id=user_id)

            if not consume_confirmation_code(user_id=user_id, code=code):
                return Response(
                    {'error': 'Неверный или просроченный код подтверждения'},
                    status=status.HTTP_400_BAD_REQUEST
                )
            user.is_active = True
            user.save()

        refresh = CustomRefreshToken.for_user(user)

        return Response(
            {
                'message': 'Аккаунт активирован',
                'refresh': str(refresh),
                'access': str(refresh.access_token),
            },
            status=status.HTTP_200_OK
        )


class AuthorizationAPIView(APIView):

    def post(self, request):
        serializer = AuthValidateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user = serializer.validated_data['user']

        if not user.is_active:
            return Response(
                {'error': 'Аккаунт не активирован'},
                status=status.HTTP_401_UNAUTHORIZED
            )

        refresh = CustomRefreshToken.for_user(user)

        return Response({
            'refresh': str(refresh),
            'access': str(refresh.access_token),
        })

class GoogleAuthorizationAPIView(APIView):

    def post(self, request):
        serializer = GoogleAuthSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user = serializer.validated_data['user']

        refresh = CustomRefreshToken.for_user(user)

        return Response({
            'refresh': str(refresh),
            'access': str(refresh.access_token),
        })