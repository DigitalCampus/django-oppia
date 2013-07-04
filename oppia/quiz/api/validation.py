# oppia/quiz/api/validation.py
from django.utils.translation import ugettext_lazy as _

from oppia.quiz.models import Quiz

from tastypie import bundle
from tastypie.validation import Validation

class QuizOwnerValidation(Validation):
    def is_valid(self, bundle, request=None):
        if not bundle.data:
            return {'__all__': 'no data.'}
        errors = {}
        quiz = bundle.obj.quiz
        if quiz.owner.id != bundle.request.user.id:
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
        # check quiz exists and is not deleted/draft etc
        try:
            quiz = Quiz.objects.get(pk=bundle.obj.quiz_id, deleted=0, draft=0)
        except Quiz.DoesNotExist:
            errors['error_message'] = _(u"Quiz does not exist")
        # check all questions actually belong to this quiz
        
        # check there is a response for every quiz question
        
        # check 

        return errors