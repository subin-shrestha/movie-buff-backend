from django.test import TestCase

from helpers.exceptions import AlreadyExists
from quiz.models import Choice
from .receipes import create_movie, create_question, create_choice


class TestChoice(TestCase):
	@classmethod
	def setUpTestData(cls):
		cls.movie = create_movie()
		cls.question = create_question(movie=cls.movie)
		cls.choice = create_choice(question=cls.question, is_correct=True)

	def test_single_correct_answer(self):
		create_choice(question=self.question, is_correct=False, _quantity=4)
		self.assertEqual(self.question.choices.count(), 5)

	def test_two_correct_answer(self):
		with self.assertRaisesMessage(AlreadyExists, "This question already have another correct answer."):
			create_choice(question=self.question, is_correct=True)

		self.assertEqual(self.question.choices.count(), 1)