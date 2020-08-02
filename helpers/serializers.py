from django.core.exceptions import ObjectDoesNotExist
from rest_framework import serializers


class BaseModelSerializer(serializers.ModelSerializer):
	idx = serializers.CharField(read_only=True)

	class Meta:
		exclude = ("id", "modified_on", "is_obsolete")
		extra_kwargs = {
			"created_on": {"read_only": True},
			"modified_on": {"read_only": True}
		}


class DetailRelatedField(serializers.RelatedField):
	"""
	Read/write serializer field for relational field.
	Syntax:
		DetailRelatedField(Model, [lookup], representation)

		Model: model to which the serializer field is related to
		lookup: field for getting a model instance, if not supplied it defaults to idx
		representation: a model instance method name for getting serialized data
	"""

	def __init__(self, model, **kwargs):
		if not kwargs.get("read_only"):
			kwargs["queryset"] = model.objects.all()

		self.lookup = kwargs.pop("lookup", None) or "idx"

		try:
			self.representation = kwargs.pop("representation")
		except KeyError:
			raise Exception("Please supply representation.")

		super().__init__(**kwargs)

	def to_internal_value(self, data):
		try:
			return self.queryset.get(**{self.lookup: data})
		except ObjectDoesNotExist:
			raise serializers.ValidationError("Object does not exist.")

	def to_representation(self, obj):
		return getattr(obj, self.representation)()
