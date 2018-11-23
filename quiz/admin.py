# oppia/quiz/admin.py
from django.contrib import admin

from models import Quiz, Question, Response, ResponseProps, QuestionProps, QuizProps, \
    QuizQuestion, QuizAttempt, QuizAttemptResponse


class QuizAttemptAdmin(admin.ModelAdmin):
    list_display = ('user', 'quiz', 'attempt_date', 'score', 'event', 'points', 'ip', 'instance_id', 'agent')


class QuestionPropsAdmin(admin.ModelAdmin):
    list_display = ('question', 'name', 'value')


class ResponsePropsAdmin(admin.ModelAdmin):
    list_display = ('response', 'name', 'value')


class QuizPropsAdmin(admin.ModelAdmin):
    list_display = ('quiz', 'name', 'value')


class QuestionAdmin(admin.ModelAdmin):
    list_display = ('owner', 'title', 'type', 'created_date', 'lastupdated_date')


class QuizAttemptResponseAdmin(admin.ModelAdmin):
    list_display = ('question', 'score', 'text')


class QuizAdmin(admin.ModelAdmin):
    list_display = ('title', 'description', 'owner', 'created_date', 'lastupdated_date', 'draft', 'deleted')


class ResponseAdmin(admin.ModelAdmin):
    list_display = ('question', 'title', 'owner', 'created_date', 'lastupdated_date', 'score', 'order')


class QuizQuestionAdmin(admin.ModelAdmin):
    list_display = ('quiz', 'question', 'order')


admin.site.register(Quiz, QuizAdmin)
admin.site.register(Question, QuestionAdmin)
admin.site.register(Response, ResponseAdmin)
admin.site.register(ResponseProps, ResponsePropsAdmin)
admin.site.register(QuestionProps, QuestionPropsAdmin)
admin.site.register(QuizProps, QuizPropsAdmin)
admin.site.register(QuizQuestion, QuizQuestionAdmin)
admin.site.register(QuizAttempt, QuizAttemptAdmin)
admin.site.register(QuizAttemptResponse, QuizAttemptResponseAdmin)
