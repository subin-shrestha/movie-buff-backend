from django.test import TestCase

from autho.tests.receipes import create_user
from quiz.tests.receipes import create_user_aggregate
from quiz.serializers import UserAggregateSerializer


class TestUserAggregateSerializer(TestCase):
	@classmethod
	def setUpTestData(cls):
		cls.user_data = {
			'idx': "testIdx",
			'username': "testUsername"
		}
		user = create_user(**cls.user_data)
		cls.aggregate_data = create_user_aggregate(
			idx="aggregateIdx",
			user=user,
			total_question=10,
			total_score=75
		)

	def test_response_data(self):
		serializer = UserAggregateSerializer(self.aggregate_data)
		data = serializer.data

		self.assertEqual(data['idx'], "aggregateIdx")
		self.assertDictEqual(data['user'], self.user_data)
		self.assertEqual(data['total_question'], 10)
		self.assertEqual(data['total_score'], 75)
