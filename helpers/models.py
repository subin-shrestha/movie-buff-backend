from django.db import models
from shortuuidfield import ShortUUIDField


class BaseModel(models.Model):
	"""Base model for possibly every other model."""
	idx = ShortUUIDField(unique=True)
	created_on = models.DateTimeField(auto_now_add=True)
	modified_on = models.DateTimeField(auto_now=True)
	is_obsolete = models.BooleanField(default=False)

	def update(self, **kwargs):
		for attr, value in kwargs.items():
			setattr(self, attr, value)
		self.save()
		return self

	def delete(self, force_delete=True, **kwargs):
		if force_delete:
			super(BaseModel, self).delete(**kwargs)
		else:
			self.update(is_obsolete=True)
			return self

	class Meta:
		abstract = True
