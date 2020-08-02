from django.contrib.auth import login, logout
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet
from rest_framework.authtoken.models import Token

from autho.models import User
from autho.serializers import SignupSerializer, VerifyOtpSerializer
from autho.helpers import get_random_string


class UserAPI(GenericViewSet):
    @action(methods=["POST"], detail=False)
    def signup(self, request, *args, **kwargs):
        """ Signup a users."""

        serializer = SignupSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        data = serializer.data
        data['code'] = get_random_string()
        user = User.objects.create_user(**data)
        user.send_email("Account OTP", f"Kindly use code {user.code} for completing signup.")
        response = {'detail': "Please verify your OTP code."}
        return Response(response, status=status.HTTP_201_CREATED)

    @action(methods=["POST"], detail=False)
    def verify_otp(self, request, *args, **kwargs):
        """ Verify OTP code."""

        serializer = VerifyOtpSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user = serializer.validated_data['code']
        user.is_verified =True
        user.code = None
        user.save()

        login(request, user)
        token, _ = Token.objects.get_or_create(user=user)

        response = {
            'detail': "User's OTP has been verified.",
            'token': token.key
        }
        return Response(response, status=status.HTTP_200_OK)

