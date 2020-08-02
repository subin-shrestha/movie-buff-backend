from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from autho.models import User
from autho.serializers import SignupSerializer
from autho.helpers import get_random_string


@api_view(["POST"])
def Signup(request, *args, **kwargs):
    """ Signup a users."""

    serializer = SignupSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)

    data = serializer.data
    data['code'] = get_random_string()
    user = User.objects.create_user(**data)
    user.send_email("Account OTP", f"Kindly use code {user.code} for completing signup.")
    response = {'detail': "Please verify your OTP code."}
    return Response(response, status=status.HTTP_201_CREATED)
