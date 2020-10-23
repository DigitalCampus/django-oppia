# oppia/quiz/admin.py
from django.contrib import admin

from quiz.models import Quiz, \
                        Question, \
                        Response, \
                        ResponseProps, \
                        QuestionProps, \
                        QuizProps, \
                        QuizQuestion, \
                        QuizAttempt, \
                        QuizAttemptResponse

from quiz import constants

class QuizAttemptAdmin(admin.ModelAdmin):
    list_display = ('user',
                    'quiz',
                    'attempt_date',
                    'score',
                    'event',
                    'points',
                    'ip',
                    'instance_id',
                    'agent')


class QuestionPropsAdmin(admin.ModelAdmin):
    list_display = ('question', 'name', 'value')


class ResponsePropsAdmin(admin.ModelAdmin):
    list_display = ('response', 'name', 'value')


class QuizPropsAdmin(admin.ModelAdmin):
    list_display = ('quiz', 'name', 'value')


class QuestionAdmin(admin.ModelAdmin):
    list_display = ('owner',
                    'title',
                    'type',
                    'created_date',
                    'lastupdated_date',
                    'no_responses',
                    'difficulty_index',
                    'discrimination_index')
    search_fields = ['title']
    
    def no_responses(self, obj):
        return obj.get_no_responses()

    def difficulty_index(self, obj):
        if obj.get_no_responses() < constants.MIN_NO_RESPONSES_FOR_INDICES:
            return "--"
        else:
            return "%0.2f" % obj.get_difficulty_index()

    def discrimination_index(self, obj):
        if obj.get_no_responses() < constants.MIN_NO_RESPONSES_FOR_INDICES:
            return "--"
        else:
            return "%0.0f %%" % obj.get_discrimination_index()


class QuizAttemptResponseAdmin(admin.ModelAdmin):
    list_display = ('question', 'score', 'text')


class QuizAdmin(admin.ModelAdmin):
    list_display = ('title',
                    'description',
                    'owner',
                    'created_date',
                    'lastupdated_date',
                    'draft',
                    'deleted')
    search_fields = ['title', 'description']


class ResponseAdmin(admin.ModelAdmin):
    list_display = ('question',
                    'title',
                    'owner',
                    'created_date',
                    'lastupdated_date',
                    'score',
                    'order')
    search_fields = ['title']


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
