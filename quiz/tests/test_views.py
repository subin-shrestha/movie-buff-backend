from unittest.mock import patch
from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework.response import Response
from rest_framework.authtoken.models import Token

from autho.tests.receipes import create_user
from quiz.tests.receipes import create_user_aggregate


class UserAggregateAPI(APITestCase):
	@classmethod
	def setUpTestData(cls):
		cls.url = reverse('user-aggregate-list')
		cls.credentials = {'username': 'test', 'password': "secret"}
		create_user_aggregate(_quantity=100)

	def test_authentication(self):
		response = self.client.get(self.url)
		json_response = response.json()

		self.assertEqual(response.status_code, 401)
		self.assertEqual(json_response.get('detail'), "Authentication credentials were not provided.")

	def test_permission(self):
		user = create_user(is_verified=False)
		token = Token.objects.create(user=user)
		self.client.force_authenticate(user)
		self.client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)

		response = self.client.get(self.url)
		json_response = response.json()
		self.assertEqual(response.status_code, 403)
		self.assertEqual(json_response.get('detail'), "You do not have permission to perform this action.")

	def test_verified(self):
		user = create_user(is_verified=True)
		token = Token.objects.create(user=user)
		self.client.force_authenticate(user)
		self.client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)

		response = self.client.get(self.url)
		json_response = response.json()
		self.assertEqual(response.status_code, 200)
		self.assertEqual(json_response['total_pages'], 2)
		self.assertEqual(json_response['total_records'], 100)
		self.assertEqual(json_response['current_page'], 1)
		self.assertEqual(json_response['next'], "http://testserver/api/user-aggregate/?page=2")
		self.assertIsInstance(json_response['records'], list)

	def test_detail_by_id(self):
		create_user_aggregate(id=200)
		url = reverse('user-aggregate-detail', args=(200,))
		user = create_user(is_verified=True)
		token = Token.objects.create(user=user)
		self.client.force_authenticate(user)
		self.client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)

		response = self.client.get(url)
		json_response = response.json()
		self.assertEqual(response.status_code, 404)
		self.assertEqual(json_response['detail'], "Not found.")

	def test_detail_by_idx(self):
		create_user_aggregate(idx="randomIdx")
		url = reverse('user-aggregate-detail', args=('randomIdx',))
		user = create_user(is_verified=True)
		token = Token.objects.create(user=user)
		self.client.force_authenticate(user)
		self.client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)

		response = self.client.get(url)
		json_response = response.json()
		self.assertEqual(response.status_code, 200)
		self.assertEqual(json_response['idx'], "randomIdx")
