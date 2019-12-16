
from django.contrib.auth.models import User
from django.utils.translation import ugettext as _
from api.resources.login import UserResource
from tastypie import fields
from tastypie.authentication import ApiKeyAuthentication
from tastypie.authorization import Authorization
from tastypie.exceptions import BadRequest
from tastypie.resources import ModelResource

from oppia import DEFAULT_IP_ADDRESS
from oppia.models import Points, Award
from quiz.api.serializers import QuizJSONSerializer, \
                                 QuizAttemptJSONSerializer
from quiz.api.validation import QuizOwnerValidation
from quiz.models import Quiz, Question, QuizQuestion, QuizAttempt, \
                        QuizAttemptResponse


class QuizResource(ModelResource):
    questions = fields.ToManyField('quiz.api.resources.QuizQuestionResource',
                                   'quizquestion_set',
                                   related_name='quiz',
                                   full=True)
    owner = fields.ForeignKey(UserResource, 'owner')

    class Meta:
        queryset = Quiz.objects.filter(draft=0,
                                       deleted=0) \
                               .order_by('-lastupdated_date')
        allowed_methods = ['get', 'post']
        fields = ['title', 'id', 'description', 'lastupdated_date']
        resource_name = 'quiz'
        include_resource_uri = True
        serializer = QuizJSONSerializer()
        authentication = ApiKeyAuthentication()
        authorization = Authorization()
        always_return_data = True

    def hydrate(self, bundle, request=None):
        bundle.obj.owner = User.objects.get(pk=bundle.request.user.id)
        return bundle


class QuizQuestionResource(ModelResource):
    question = fields.ToOneField('quiz.api.resources.QuestionResource',
                                 'question',
                                 full=True)

    class Meta:
        queryset = QuizQuestion.objects.all()
        allowed_methods = ['get', 'post']
        fields = ['id', 'order', 'question']
        include_resource_uri = False
        authentication = ApiKeyAuthentication()
        authorization = Authorization()
        validation = QuizOwnerValidation()
        always_return_data = True

    def hydrate(self, bundle, request=None):
        bundle.obj.quiz_id = QuizResource() \
            .get_via_uri(bundle.data['quiz']).id
        return bundle


class QuestionResource(ModelResource):

    class Meta:
        queryset = Question.objects.all()
        allowed_methods = ['get', 'post']
        fields = ['title', 'type', 'id']
        resource_name = 'question'
        include_resource_uri = True
        authentication = ApiKeyAuthentication()
        authorization = Authorization()
        always_return_data = True

    def hydrate(self, bundle, request=None):
        bundle.obj.owner = User.objects.get(pk=bundle.request.user.id)
        return bundle


class QuizAttemptResponseResource(ModelResource):
    question = fields.ForeignKey(QuestionResource, 'question')
    quizattempt = fields.ToOneField('quiz.api.resources.QuizAttemptResource',
                                    'quizattempt',
                                    related_name='quizattemptresponse')

    class Meta:
        queryset = QuizAttemptResponse.objects.all()
        resource_name = 'quizattemptresponse'
        allowed_methods = ['post']
        authentication = ApiKeyAuthentication()
        authorization = Authorization()


class QuizAttemptResource(ModelResource):
    quiz = fields.ForeignKey(QuizResource, 'quiz')
    responses = fields \
        .ToManyField('quiz.api.resources.QuizAttemptResponseResource',
                     'quizattemptresponse_set',
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
        bundle.obj.user = User.objects.get(pk=bundle.request.user.id)
        bundle.obj.ip = bundle.request.META.get('REMOTE_ADDR',
                                                DEFAULT_IP_ADDRESS)
        bundle.obj.agent = bundle.request.META.get('HTTP_USER_AGENT',
                                                   'unknown')

        # check the quiz exists
        try:
            bundle.obj.quiz = Quiz.objects.get(pk=bundle.data['quiz_id'])
        except Quiz.DoesNotExist:
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
                    raise BadRequest(_(u'Question does not exist'))
                # check part of this quiz
                try:
                    QuizQuestion.objects.get(quiz=bundle.obj.quiz,
                                             question=response['question'])
                except QuizQuestion.DoesNotExist:
                    raise BadRequest(
                        _(u'This question is not part of this quiz'))

        if 'points' in bundle.data:
            bundle.obj.points = bundle.data['points']

        if 'event' in bundle.data:
            bundle.obj.event = bundle.data['event']

        return bundle

    def dehydrate_points(self, bundle):
        points = Points.get_userscore(bundle.request.user)
        return points

    def dehydrate_badges(self, bundle):
        badges = Award.get_userawards(bundle.request.user)
        return badges
