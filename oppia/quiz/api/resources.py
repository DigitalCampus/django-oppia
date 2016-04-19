# oppia/quiz/api/resources.py
from django.conf.urls import url
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django.core.paginator import Paginator, InvalidPage
from django.db import IntegrityError
from django.db.models import Q
from django.http.response import Http404
from django.utils.translation import ugettext as _

from tastypie import fields, bundle, http
from tastypie.authentication import Authentication, ApiKeyAuthentication
from tastypie.authorization import Authorization
from tastypie.exceptions import NotFound, BadRequest, InvalidFilterError, HydrationError, InvalidSortError, ImmediateHttpResponse
from tastypie.models import ApiKey
from tastypie.resources import ModelResource

from oppia.models import Points, Award
from oppia.api.resources import UserResource
from oppia.api.serializers import PrettyJSONSerializer
from oppia.quiz.api.serializers import QuizJSONSerializer, QuizAttemptJSONSerializer
from oppia.quiz.api.validation import QuizOwnerValidation, QuestionOwnerValidation
from oppia.quiz.api.validation import ResponseOwnerValidation, QuizAttemptValidation
from oppia.quiz.models import Quiz, Question, QuizQuestion, Response, QuestionProps
from oppia.quiz.models import QuizProps, ResponseProps, QuizAttempt, QuizAttemptResponse
   
          
class QuizResource(ModelResource):
    questions = fields.ToManyField('oppia.quiz.api.resources.QuizQuestionResource', 'quizquestion_set', related_name='quiz', full=True)
    props = fields.ToManyField('oppia.quiz.api.resources.QuizPropsResource', 'quizprops_set', related_name='quiz', full=True)
    owner = fields.ForeignKey(UserResource, 'owner')
    class Meta:
        queryset = Quiz.objects.filter(draft=0,deleted=0).order_by('-lastupdated_date')
        allowed_methods = ['get','post']
        fields = ['title', 'id', 'description', 'lastupdated_date']
        resource_name = 'quiz'
        include_resource_uri = True
        serializer = QuizJSONSerializer()  
        authentication = ApiKeyAuthentication()
        authorization = Authorization()
        always_return_data = True
        
    def hydrate(self, bundle, request=None):
        bundle.obj.owner = User.objects.get(pk = bundle.request.user.id)
        return bundle 
    
    def prepend_urls(self):
        return [
            url(r"^(?P<resource_name>%s)/search/$" % self._meta.resource_name, self.wrap_view('get_search'), name="api_get_search"),
        ]
        
    def get_search(self, request, **kwargs):
        self.method_check(request, allowed=['get'])
        self.is_authenticated(request)
        self.throttle_check(request)

        # Do the query.
        query = request.GET.get('q', '')
        searchresults = self._meta.queryset.filter(draft=0,deleted=0).filter(Q(title__icontains=query) | Q(description__icontains=query))
        paginator = Paginator(searchresults, 20)

        try:
            page = paginator.page(int(request.GET.get('page', 1)))
        except InvalidPage:
            raise Http404("Sorry, no results on that page.")

        objects = []

        for result in page.object_list:
            bundle = self.build_bundle(obj=result, request=request)
            bundle = self.full_dehydrate(bundle)
            objects.append(bundle)

        object_list = {
            'objects': objects,
        }

        self.log_throttled_access(request)
        return self.create_response(request, object_list)
    
        
class QuizQuestionResource(ModelResource):
    question = fields.ToOneField('oppia.quiz.api.resources.QuestionResource', 'question', full=True)
    class Meta:
        queryset = QuizQuestion.objects.all()
        allowed_methods = ['get','post']
        fields = ['id','order','question']
        include_resource_uri = False
        authentication = ApiKeyAuthentication()
        authorization = Authorization()
        validation = QuizOwnerValidation()
        always_return_data = True
      
    def hydrate(self, bundle, request=None):
        bundle.obj.quiz_id = QuizResource().get_via_uri(bundle.data['quiz']).id
        return bundle
     
class QuestionResource(ModelResource):
    responses = fields.ToManyField('oppia.quiz.api.resources.ResponseResource', 'response_set', related_name='question', full=True)   
    props = fields.ToManyField('oppia.quiz.api.resources.QuestionPropsResource', 'questionprops_set', related_name='question', full=True, null=True)
    owner = fields.ForeignKey(UserResource, 'owner')
    class Meta:
        queryset = Question.objects.all()
        allowed_methods = ['get','post']
        fields = ['title','type','id']
        resource_name = 'question'
        include_resource_uri = True
        authentication = ApiKeyAuthentication()
        authorization = Authorization()
        always_return_data = True

    def hydrate(self, bundle, request=None):
        bundle.obj.owner = User.objects.get(pk = bundle.request.user.id)
        return bundle   
 
class QuestionPropsResource(ModelResource):
    question = fields.ToOneField('oppia.quiz.api.resources.QuestionResource', 'question', related_name='questionprops')
    class Meta:
        queryset = QuestionProps.objects.all()
        allowed_methods = ['get','post']
        resource_name = 'questionprops'
        include_resource_uri = True
        authentication = ApiKeyAuthentication()  
        authorization = Authorization()
        validation = QuestionOwnerValidation()
        always_return_data = True
 
    
class ResponseResource(ModelResource):
    question = fields.ForeignKey(QuestionResource, 'question')
    props = fields.ToManyField('oppia.quiz.api.resources.ResponsePropsResource', 'responseprops_set', related_name='response', full=True, null=True)
    class Meta:
        queryset = Response.objects.all()
        allowed_methods = ['get','post']
        fields = ['id','order', 'title','score']
        resource_name = 'response'
        include_resource_uri = True
        serializer = PrettyJSONSerializer()
        authentication = ApiKeyAuthentication()
        authorization = Authorization()
        validation = QuestionOwnerValidation()
        always_return_data = True
        
    def hydrate(self, bundle, request=None):
        bundle.obj.owner = User.objects.get(pk = bundle.request.user.id)
        return bundle 
 
class ResponsePropsResource(ModelResource):
    response = fields.ToOneField('oppia.quiz.api.resources.ResponseResource', 'response', related_name='responseprops')
    class Meta:
        queryset = ResponseProps.objects.all()
        allowed_methods = ['get','post']
        fields = ['name', 'value']
        resource_name = 'responseprops'
        include_resource_uri = False
        authentication = ApiKeyAuthentication()  
        authorization = Authorization()
        validation = ResponseOwnerValidation()
        always_return_data = True            

           
class QuizPropsResource(ModelResource):
    quiz = fields.ForeignKey(QuizResource, 'quiz')
    class Meta:
        queryset = QuizProps.objects.all()
        allowed_methods = ['get','post']
        resource_name = 'quizprops'
        include_resource_uri = True
        authentication = ApiKeyAuthentication()  
        authorization = Authorization()
        validation = QuizOwnerValidation()
        always_return_data = True
    
    def hydrate(self, bundle, request=None):        
        # check the quiz exists
        if 'quiz_id' in bundle.data:
            try:
                bundle.obj.quiz = Quiz.objects.get(pk = bundle.data['quiz_id'])
            except Quiz.DoesNotExist:
                raise BadRequest(_(u'Quiz does not exist'))
        return bundle
        
    # add the quiz_id into the bundle
    def dehydrate(self, bundle, request=None):
        bundle.data['quiz_id'] = QuizResource().get_via_uri(bundle.data['quiz']).id 
        return bundle
    
    # use this for filtering on the digest prop of a quiz to determine if it already exists
    # to avoid recreating the same quiz over and over
    
    def prepend_urls(self):
        return [
            url(r"^(?P<resource_name>%s)/digest/(?P<digest>[\w\d_.-]+)/$" % self._meta.resource_name, self.wrap_view('digest_detail'), name="api_digest_detail"),
        ]
        
    def digest_detail(self, request, **kwargs):
        self.method_check(request, allowed=['get'])
        self.is_authenticated(request)
        self.throttle_check(request)
        
        digest = kwargs.pop('digest', None)
        quizprop = self._meta.queryset.filter(name = 'digest',quiz__deleted=0,quiz__draft=0).filter(value=digest)
        paginator = Paginator(quizprop, 20)

        try:
            page = paginator.page(int(request.GET.get('page', 1)))
        except InvalidPage:
            raise Http404("Sorry, no results on that page.")
        
        objects = []

        for result in page.object_list:
            bundle = self.build_bundle(obj=result, request=request)
            bundle = self.full_dehydrate(bundle)
            objects.append(bundle)

        object_list = {
            'quizzes': objects,
        }

        self.log_throttled_access(request)
        return self.create_response(request, object_list)
    
class QuizAttemptResponseResource(ModelResource):
    question = fields.ForeignKey(QuestionResource, 'question')
    quizattempt = fields.ToOneField('oppia.quiz.api.resources.QuizAttemptResource', 'quizattempt', related_name='quizattemptresponse')
    class Meta:
        queryset = QuizAttemptResponse.objects.all()
        # TODO how to put slash in the name?
        resource_name = 'quizattemptresponse'
        allowed_methods = ['post']
        authentication = ApiKeyAuthentication()
        authorization = Authorization()    
           
class QuizAttemptResource(ModelResource):
    quiz = fields.ForeignKey(QuizResource, 'quiz')
    user = fields.ForeignKey(UserResource, 'user')
    responses = fields.ToManyField('oppia.quiz.api.resources.QuizAttemptResponseResource', 'quizattemptresponse_set', related_name='quizattempt', full=True, null=True)
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
        bundle.obj.user = User.objects.get(pk = bundle.request.user.id)
        bundle.obj.ip = bundle.request.META.get('REMOTE_ADDR','0.0.0.0')
        bundle.obj.agent = bundle.request.META.get('HTTP_USER_AGENT','unknown')
        
        # check the quiz exists
        try:
            bundle.obj.quiz = Quiz.objects.get(pk = bundle.data['quiz_id'])
        except Quiz.DoesNotExist:
            raise BadRequest(_(u'Quiz does not exist'))    
        
        # see if instance id already submitted
        attempts = QuizAttempt.objects.filter(instance_id = bundle.data['instance_id']).count()
        
        if attempts > 0:
            raise BadRequest(_(u'QuizAttempt already submitted')) 
        
        #check that all the questions exist and are part of this quiz
        for response in bundle.data['responses']:
            if 'question_id' in response:
                try:
                    response['question'] = Question.objects.get(pk = response['question_id'])
                except Question.DoesNotExist:
                    raise BadRequest(_(u'Question does not exist'))
                #check part of this quiz
                try:
                    QuizQuestion.objects.get(quiz=bundle.obj.quiz,question=response['question'])
                except QuizQuestion.DoesNotExist:
                    raise BadRequest(_(u'This question is not part of this quiz'))
            
        return bundle
    
    def dehydrate_points(self,bundle):
        points = Points.get_userscore(bundle.request.user)
        return points
    
    def dehydrate_badges(self,bundle):
        badges = Award.get_userawards(bundle.request.user)
        return badges
    