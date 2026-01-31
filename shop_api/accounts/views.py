import random
import string

from django.db import transaction
from django.contrib.auth import authenticate

from rest_framework.views import APIView
from rest_framework.generics import CreateAPIView
from rest_framework.response import Response
from rest_framework import status

from .models import CustomUser, ConfirmationCode
from .serializers import (
    RegisterValidateSerializer,
    AuthValidateSerializer,
    ConfirmationSerializer
)
from .tokens import CustomRefreshToken


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

            ConfirmationCode.objects.create(
                user=user,
                code=code
            )

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
            confirmation = ConfirmationCode.objects.get(
                user_id=user_id,
                code=code
            )
            user = confirmation.user
            user.is_active = True
            user.save()

            confirmation.delete()

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