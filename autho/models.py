import os
from django.core.mail import send_mail
from django.conf import settings
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.template.loader import render_to_string

from autho.helpers import get_random_string
from helpers.exceptions import UserAlreadyVerified

TEMPLATE_DIR = os.path.join(settings.BASE_DIR, 'autho/templates')


class User(AbstractUser):
	code = models.CharField(max_length=6, unique=True, null=True, blank=True)
	is_verified = models.BooleanField(default=False)

	def __str__(self):
		return self.username

	def send_email(self, subject, message, from_email=None, **kwargs):
		"""Send an email to this user."""
		from_email = from_email or settings.ADMIN_EMAIL
		send_mail(subject, message, from_email, [self.email], **kwargs)

	def verify(self, title=None, message=None):
		""" Verify and send password to user email."""
		if self.is_verified is True:
			raise UserAlreadyVerified

		password = get_random_string()
		self.is_verified =True
		self.code = None
		self.set_password(password)
		self.save()

		data = {
			'username': self.username,
			'password': password
		}
		html_msg = render_to_string(f"{TEMPLATE_DIR}/account_verify.html", data)

		self.send_email(title, message, html_message=html_msg)