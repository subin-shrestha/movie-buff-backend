from django.db import models
from django.contrib.auth.models import AbstractUser

from autho.helpers import get_random_string


class User(AbstractUser):
	code = models.CharField(max_length=6)

	def save(self, *args, **kwargs):
		if not self.pk:
			self.code = get_random_string()
		return super().save(*args, **kwargs)
