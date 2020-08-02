from django.db import models

from autho.models import User
from helpers.models import BaseModel
from helpers.exceptions import AlreadyExists


class Movie(BaseModel):
	title = models.CharField(max_length=100)
	kind = models.CharField(max_length=50)
	year = models.IntegerField(blank=True, null=True)
	image = models.URLField(max_length=300)

	def __str__(self):
		return self.title


class Question(BaseModel):
	movie = models.ForeignKey(
		"quiz.Movie",
		related_name="questions",
		on_delete=models.CASCADE
	)
	title = models.CharField(max_length=200)
	score = models.IntegerField()

	def __str__(self):
		return self.title


class Choice(BaseModel):
	question = models.ForeignKey(
		"quiz.Question",
		related_name="choices",
		on_delete=models.PROTECT
	)
	value = models.CharField(max_length=150)
	is_correct = models.BooleanField(default=False)

	def __str__(self):
		return self.value

	def save(self, **kwargs):
		if self.is_correct is True:
			filters = {
				'is_obsolete': False,
				'is_correct': True,
				'question_id': self.question_id
			}
			correct_choices = Choice.objects.filter(**filters).exclude(id=self.id)
			if correct_choices.exists():
				raise AlreadyExists("This question already have another correct answer.")
		return super().save(**kwargs)


class Answer(BaseModel):
	user = models.ForeignKey(
		"autho.User",
		related_name="answers",
		on_delete=models.PROTECT
	)
	question = models.ForeignKey(
		"quiz.Question",
		related_name="answers",
		on_delete=models.PROTECT
	)
	choice = models.ForeignKey(
		"quiz.Choice",
		related_name="choices",
		on_delete=models.CASCADE
	)

	def __str__(self):
		return f"{self.question} -> {self.choice}"


class UserAggregate(BaseModel):
	user = models.ForeignKey(
		"autho.User",
		related_name="aggregates",
		on_delete=models.PROTECT
	)
	total_question = models.IntegerField()
	total_score = models.IntegerField()

	def __str__(self):
		return self.idx

