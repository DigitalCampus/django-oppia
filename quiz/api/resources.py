
from django.contrib.auth.models import User
from django.utils.translation import gettext as _
from tastypie import fields
from tastypie.authentication import ApiKeyAuthentication
from tastypie.authorization import Authorization
from tastypie.exceptions import BadRequest
from tastypie.resources import ModelResource

from datarecovery.models import DataRecovery
from oppia import DEFAULT_IP_ADDRESS
from oppia.models import Points, Award
from quiz.api.serializers import QuizAttemptJSONSerializer
from quiz.models import Quiz, Question, QuizQuestion, QuizAttempt, \
                        QuizAttemptResponse


class QuizAttemptResponseResource(ModelResource):
    quizattempt = fields.ToOneField('quiz.api.resources.QuizAttemptResource',
                                    'quizattempt',
                                    related_name='quizattemptresponse')

    class Meta:
        queryset = QuizAttemptResponse.objects.all()
        resource_name = 'quizattemptresponse'
        allowed_methods = ['post']
        authentication = ApiKeyAuthentication()
        authorization = Authorization()

    def hydrate(self, bundle, request=None):
        try:
            bundle.obj.question = Question.objects.get(
                pk=bundle.data['question_id'])
        except Question.DoesNotExist:
            raise BadRequest(_(u'Question does not exist'))
        return bundle


class QuizAttemptResource(ModelResource):
    responses = fields.ToManyField(QuizAttemptResponseResource,
                                   'responses',
                                   related_name='quizattempt',
                                   full=True,
                                   null=True)
    points = fields.IntegerField(readonly=True)
    badges = fields.IntegerField(readonly=True)

    class Meta:
        queryset = QuizAttempt.objects.all()
        resource_name = 'quizattempt'
        allowed_methods = ['post']
        authentication = ApiKeyAuthentication()
        authorization = Authorization()
        always_return_data = True
        serializer = QuizAttemptJSONSerializer()

    def hydrate(self, bundle, request=None):
        errors = []
        bundle.obj.user = User.objects.get(pk=bundle.request.user.id)
        bundle.obj.ip = bundle.request.META.get('REMOTE_ADDR',
                                                DEFAULT_IP_ADDRESS)
        bundle.obj.agent = bundle.request.META.get('HTTP_USER_AGENT',
                                                   'unknown')

        # check the quiz exists
        try:
            bundle.obj.quiz = Quiz.objects.get(pk=bundle.data['quiz_id'])
        except Quiz.DoesNotExist:
            errors.append(DataRecovery.Reason.QUIZ_DOES_NOT_EXIST)
            raise BadRequest(_(u'Quiz does not exist'))

        # see if instance id already submitted
        attempts = QuizAttempt.objects.filter(
            instance_id=bundle.data['instance_id']).count()

        if attempts > 0:
            raise BadRequest(_(u'QuizAttempt already submitted'))

        # check that all the questions exist and are part of this quiz
        for response in bundle.data['responses']:
            if 'question_id' in response:
                try:
                    response['question'] = Question.objects.get(
                        pk=response['question_id'])
                except Question.DoesNotExist:
                    errors.append(DataRecovery.Reason.QUESTION_DOES_NOT_EXIST)
                    raise BadRequest(_(u'Question does not exist'))
                # check part of this quiz
                try:
                    QuizQuestion.objects.get(quiz=bundle.obj.quiz,
                                             question=response['question'])
                except QuizQuestion.DoesNotExist:
                    errors.append(DataRecovery.Reason.QUESTION_FROM_DIFFERENT_QUIZ)
                    raise BadRequest(
                        _(u'This question is not part of this quiz'))

        if 'points' in bundle.data:
            bundle.obj.points = bundle.data['points']

        if 'event' in bundle.data:
            bundle.obj.event = bundle.data['event']

        if 'timetaken' in bundle.data:
            bundle.obj.time_taken = bundle.data['timetaken']

        return bundle

    def dehydrate_points(self, bundle):
        points = Points.get_userscore(bundle.request.user)
        return points

    def dehydrate_badges(self, bundle):
        badges = Award.get_userawards(bundle.request.user)
        return badges
