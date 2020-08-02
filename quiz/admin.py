from django.contrib import admin

from quiz import models


@admin.register(models.Movie)
class MovieAdmin(admin.ModelAdmin):
	list_display = ('title', 'kind', 'year')

@admin.register(models.Question)
class QuestionAdmin(admin.ModelAdmin):
	list_display = ('title', 'score')


@admin.register(models.Choice)
class ChoiceAdmin(admin.ModelAdmin):
	list_display = ('question', 'value', 'is_correct')

@admin.register(models.Answer)
class AnswerAdmin(admin.ModelAdmin):
	list_display = ('user', 'question')


@admin.register(models.UserAggregate)
class UserAggregateAdmin(admin.ModelAdmin):
	list_display = ('user', 'total_question', 'total_score')
