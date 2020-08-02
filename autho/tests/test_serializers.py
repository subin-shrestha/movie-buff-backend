from django.test import TestCase
from django.test.client import RequestFactory

from autho.serializers import SignupSerializer
from .receipes import create_user


class TestSignupSerializer(TestCase):

	def test_required_fields(self):
		serializer = SignupSerializer(data={})
		is_valid = serializer.is_valid()
		errors = serializer.errors

		self.assertFalse(is_valid, "Should return False")
		self.assertIsNotNone(errors.get('username'), "Username is required field!")
		self.assertEqual(str(errors['username'][0]), "This field is required.")
		self.assertIsNotNone(errors.get('email'), "Email is required field!")
		self.assertEqual(str(errors['email'][0]), "This field is required.")

	def test_username_exist(self):
		user = create_user(username="testname")

		data = {'username': "testname", 'email': "test@info.com"}

		serializer = SignupSerializer(data=data)
		is_valid = serializer.is_valid()
		errors = serializer.errors

		self.assertFalse(is_valid, "Should return False")
		self.assertEqual(str(errors['username'][0]), "A user with that username already exists.")

	def test_valid_data(self):
		data = {'username': "testname", 'email': "test@info.com"}
		serializer = SignupSerializer(data=data)
		is_valid = serializer.is_valid()

		self.assertTrue(is_valid, "Should return True")
		self.assertDictEqual(serializer.validated_data, data)