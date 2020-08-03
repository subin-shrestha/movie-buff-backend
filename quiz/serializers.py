from rest_framework import serializers

from autho.models import User
from quiz.models import UserAggregate
from helpers.serializers import BaseModelSerializer, DetailRelatedField


class UserAggregateSerializer(BaseModelSerializer):
	user = DetailRelatedField(User, representation="get_basic_info")

	class Meta:
		model = UserAggregate
		fields = ('idx', 'user', 'total_question', 'total_score')
