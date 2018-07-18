# oppia/quiz/api/validation.py
from django.utils.translation import ugettext_lazy as _

from tastypie.validation import Validation


class QuizOwnerValidation(Validation):
    def is_valid(self, bundle, request=None):
        if not bundle.data:
            return {'__all__': 'no data.'}
        errors = {}
        quiz = bundle.obj.quiz
        if not bundle.request.user.is_staff and quiz.owner.id != bundle.request.user.id:
            errors['error_message'] = _(u"You are not the owner of this quiz")
        return errors


class QuestionOwnerValidation(Validation):
    def is_valid(self, bundle, request=None):
        if not bundle.data:
            return {'__all__': 'no data.'}
        errors = {}
        question = bundle.obj.question
        if question.owner.id != bundle.request.user.id:
            errors['error_message'] = _(u"You are not the owner of this question")
        return errors


class ResponseOwnerValidation(Validation):
    def is_valid(self, bundle, request=None):
        if not bundle.data:
            return {'__all__': 'no data.'}
        errors = {}
        response = bundle.obj.response
        if response.owner.id != bundle.request.user.id:
            errors['error_message'] = _(u"You are not the owner of this response")
        return errors


class QuizAttemptValidation(Validation):

    def is_valid(self, bundle, request=None):
        if not bundle.data:
            return {'__all__': 'no data.'}
        errors = {}
        # check all questions actually belong to this quiz

        # check there is a response for every quiz question

        # check marks awarded are consistent with the results stored here

        return errors
