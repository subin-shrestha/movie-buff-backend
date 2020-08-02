from django.contrib import admin

from quiz.models import Question, Choice, Answer


@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    list_display = ('title', 'score')


@admin.register(Choice)
class ChoiceAdmin(admin.ModelAdmin):
    list_display = ('question', 'value', 'is_correct')

@admin.register(Answer)
class AnswerAdmin(admin.ModelAdmin):
    list_display = ('user', 'question')

