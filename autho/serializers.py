from django.core.validators import MinLengthValidator
from rest_framework import serializers

from autho.models import User


class SignupSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(required=True)

    class Meta:
        model = User
        fields = ('username', 'email')
