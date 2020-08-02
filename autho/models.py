from django.core.mail import send_mail
from django.conf import settings
from django.db import models
from django.contrib.auth.models import AbstractUser

from autho.helpers import get_random_string


class User(AbstractUser):
	code = models.CharField(max_length=6, unique=True, null=True, blank=True)
	is_verified = models.BooleanField(default=False)

	def __str__(self):
		return self.username

	def send_email(self, subject, message, from_email=None, **kwargs):
		"""Send an email to this user."""
		from_email = from_email or settings.ADMIN_EMAIL
		send_mail(subject, message, from_email, [self.email], **kwargs)

