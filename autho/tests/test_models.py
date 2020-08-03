from unittest.mock import patch
from django.test import TestCase
from django.conf import settings
from django.core import mail

from helpers.exceptions import UserAlreadyVerified
from .receipes import create_user


class TestUser(TestCase):
	@classmethod
	def setUpTestData(cls):
		cls.user = create_user(
			username="testuser",
			email='user@info.com',
			password='password'
		)

	def test_str(self):
		self.assertEqual(str(self.user), "testuser")

	def test_default_mail(self):
		settings.ADMIN_EMAIL = "admin@info.com"
		self.user.send_email("Test Subject", "Test message")
		self.assertEqual(len(mail.outbox), 1)
		self.assertEqual(mail.outbox[0].subject, "Test Subject")
		self.assertEqual(mail.outbox[0].from_email, "admin@info.com")
		self.assertEqual(mail.outbox[0].to, ["user@info.com"])
		self.assertEqual(mail.outbox[0].body, "Test message")

	def test_mail_from(self):
		self.user.send_email("Test Subject", "Test message", "sender@info.com")
		self.assertEqual(len(mail.outbox), 1)
		self.assertEqual(mail.outbox[0].subject, "Test Subject")
		self.assertEqual(mail.outbox[0].from_email, "sender@info.com")
		self.assertEqual(mail.outbox[0].to, ["user@info.com"])
		self.assertEqual(mail.outbox[0].body, "Test message")


	def test_verify_exception(self):
		user = create_user(is_verified=True)
		with self.assertRaises(UserAlreadyVerified):
			user.verify()

	@patch('autho.models.User.send_email')
	def test_verify(self, send_email):
		user = create_user(is_verified=False)
		user.set_password('obsolete')
		user.verify("title", "message")
		user.refresh_from_db()

		self.assertTrue(user.is_verified, "Should be True!")
		self.assertIsNone(user.code, "Should be None!")
		self.assertFalse(user.check_password('obsolete'))

		send_email.assert_called_once()



	def test_get_basic_info(self):
		user = create_user(idx="randomtext", username="randomusername")

		data = user.get_basic_info()
		self.assertIsInstance(data, dict)
		self.assertEqual(data['idx'], "randomtext")
		self.assertEqual(data['username'], "randomusername")
