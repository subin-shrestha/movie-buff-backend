from unittest.mock import patch
from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework.response import Response

from autho.models import User
from autho.views import ResponseMixin
from .receipes import create_user


class TestResponseMixin(TestCase):
	def setUp(self):
		self.instance = ResponseMixin()

	def test_success_instance(self):
		response = self.instance.api_success_response({})
		self.assertIsInstance(response, Response)

	def test_default_success(self):
		response = self.instance.api_success_response({})

		self.assertDictEqual(response.data, {})
		self.assertEqual(response.status_code, 200)

	def test_success_data(self):
		data = {'detail': "Success"}
		response = self.instance.api_success_response(data)

		self.assertDictEqual(response.data, data)
		self.assertEqual(response.status_code, 200)

	def test_success_status(self):
		data = {'detail': "Success"}
		response = self.instance.api_success_response(data, status=201)

		self.assertDictEqual(response.data, data)
		self.assertEqual(response.status_code, 201)


	def test_default_error(self):
		response = self.instance.api_error_response({})

		self.assertDictEqual(response.data, {})
		self.assertEqual(response.status_code, 400)

	def test_error_data(self):
		data = {'detail': "Error"}
		response = self.instance.api_error_response(data)

		self.assertDictEqual(response.data, data)
		self.assertEqual(response.status_code, 400)

	def test_error_status(self):
		data = {'detail': "Error"}
		response = self.instance.api_error_response(data, status=403)

		self.assertDictEqual(response.data, data)
		self.assertEqual(response.status_code, 403)



class TestSignup(APITestCase):
	@classmethod
	def setUpTestData(cls):
		cls.url = reverse('user-signup')

	@patch('autho.models.User.send_email')
	def test_success(self, send_email):
		data = {'username': "test", 'email': "test@info.com"}
		response = self.client.post(self.url, data=data)
		json_response = response.json()

		self.assertEqual(response.status_code, 201)
		self.assertEqual(json_response.get('detail'), "Please verify your OTP code.")
		self.assertEqual(User.objects.count(), 1)

		user = User.objects.last()
		self.assertFalse(user.is_verified)
		self.assertIsNotNone(user.code)

		send_email.assert_called_once()
		send_email.assert_called_with("Account OTP", f"Kindly use code {user.code} for completing signup.")


class TestVerifyOTP(APITestCase):
	@classmethod
	def setUpTestData(cls):
		cls.url = reverse('user-verify-otp')

	def test_success(self):
		user = create_user(code="ORANGE")
		response = self.client.post(self.url, data={'code': "ORANGE"})
		json_response = response.json()

		self.assertEqual(response.status_code, 200)
		self.assertEqual(json_response.get('detail'), "User's OTP has been verified.")
		self.assertIsNotNone(json_response.get('token'),"Token should not be none.")

		user.refresh_from_db()
		self.assertTrue(user.is_verified)
		self.assertIsNone(user.code)
		self.assertTrue(user.is_authenticated)
		self.assertIsNotNone(user.auth_token)


class TestLogin(APITestCase):
	@classmethod
	def setUpTestData(cls):
		cls.url = reverse('user-login')
		cls.credentials = {'username': 'test', 'password': "secret"}

	def test_invalid_user(self):
		response = self.client.post(self.url, data=self.credentials)
		json_response = response.json()

		self.assertEqual(response.status_code, 400)
		self.assertEqual(json_response.get('detail'), "User credential does not match.")
		self.assertIsNone(json_response.get('token'))

	def test_unverified_user(self):
		create_user(is_verified=False, **self.credentials)
		response = self.client.post(self.url, data=self.credentials)
		json_response = response.json()

		self.assertEqual(response.status_code, 400)
		self.assertEqual(json_response.get('detail'), "User has not verified yet.")
		self.assertIsNone(json_response.get('token'))

	def test_verified_user(self):
		user =create_user(is_verified=True, **self.credentials)
		response = self.client.post(self.url, data=self.credentials)
		json_response = response.json()

		self.assertEqual(response.status_code, 200)
		self.assertEqual(json_response.get('detail'), "User has been logged in.")
		self.assertIsNotNone(json_response.get('token'))
