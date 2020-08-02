from django.test import TestCase
from django.conf import settings
from django.core import mail

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
