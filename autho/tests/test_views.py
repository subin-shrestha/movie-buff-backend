from unittest.mock import patch
from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from autho.models import User
from .receipes import create_user


class TestSignup(APITestCase):
	@classmethod
	def setUpTestData(cls):
		cls.url = reverse('user-signup')

	@patch('autho.models.User.send_email')
	def test_success(self, send_email):
		data = {'username': "test", 'email': "test@info.com"}
		response = self.client.post(self.url, data=data)
		json_response = response.json()

		self.assertEqual(response.status_code, status.HTTP_201_CREATED)
		self.assertEqual(json_response.get('detail'), "Please verify your OTP code.")
		self.assertEqual(User.objects.count(), 1)

		user = User.objects.last()
		self.assertFalse(user.is_verified)
		self.assertIsNotNone(user.code)

		send_email.assert_called_once()
		send_email.assert_called_with("Account OTP", f"Kindly use code {user.code} for completing signup.")

