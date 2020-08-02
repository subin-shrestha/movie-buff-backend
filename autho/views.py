from django.contrib.auth import login, logout, authenticate
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet
from rest_framework.authtoken.models import Token

from autho.models import User
from autho.serializers import SignupSerializer, VerifyOtpSerializer, LoginSerializer
from autho.helpers import get_random_string
from autho.exceptions import CustomException


class ResponseMixin:
	def api_success_response(self, data, status=status.HTTP_200_OK):
		return Response(data, status)

	def api_error_response(self, data, status=status.HTTP_400_BAD_REQUEST):
		return Response(data, status)


class UserAPI(ResponseMixin, GenericViewSet):
	@action(methods=["POST"], detail=False)
	def signup(self, request, *args, **kwargs):
		""" Signup a users."""

		serializer = SignupSerializer(data=request.data)
		serializer.is_valid(raise_exception=True)

		data = serializer.data
		data['code'] = get_random_string()
		user = User.objects.create_user(**data)
		user.send_email("Account OTP", f"Kindly use code {user.code} for completing signup.")
		data = {'detail': "Please verify your OTP code."}
		return self.api_success_response(data, status=status.HTTP_201_CREATED)

	@action(methods=["POST"], detail=False)
	def verify_otp(self, request, *args, **kwargs):
		""" Verify OTP code."""

		serializer = VerifyOtpSerializer(data=request.data)
		serializer.is_valid(raise_exception=True)
		user = serializer.validated_data['code']
		try:
			user.verify()
		except CustomException as exp:
			return self.api_error_response({'detail': exp.message, 'error_key': exp.error_key})

		login(request, user)
		token, _ = Token.objects.get_or_create(user=user)

		data = {
			'detail': "User's OTP has been verified.",
			'token': token.key
		}
		return self.api_success_response(data)


	@action(methods=["POST"], detail=False)
	def login(self, request, *args, **kwargs):
		""" User login with credentials."""

		serializer = LoginSerializer(data=request.data)
		serializer.is_valid(raise_exception=True)

		credentials = serializer.validated_data
		user = authenticate(request, **credentials)

		if user is None:
			return self.api_error_response({'detail': "User credential does not match."})
		elif user.is_verified is False:
			return self.api_error_response({'detail': "User has not verified yet."})

		login(request, user)
		token, _ = Token.objects.get_or_create(user=user)

		data = {
			'detail': "User has been logged in.",
			'token': token.key
		}
		return self.api_success_response(data)