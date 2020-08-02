from django.core.exceptions import ObjectDoesNotExist
from django.core.validators import MinLengthValidator
from rest_framework import serializers

from autho.models import User


class SignupSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(required=True)

    class Meta:
        model = User
        fields = ('username', 'email')


class VerifyOtpSerializer(serializers.Serializer):
    code = serializers.CharField()

    def validate_code(self, value):
        try:
            user = User.objects.get(code=value)
        except ObjectDoesNotExist:
            raise serializers.ValidationError("OTP code does not match.")

        return user
