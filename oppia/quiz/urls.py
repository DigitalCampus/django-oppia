# oppia/quiz/urls.py
from django.conf.urls import patterns, include, url

from tastypie.api import Api
from oppia.quiz.api.resources import QuizResource, QuizPropsResource, QuestionResource, QuizQuestionResource, ResponseResource, QuizAttemptResource

v1_api = Api(api_name='v1')
v1_api.register(QuizResource())
v1_api.register(QuizPropsResource())
v1_api.register(QuestionResource())
v1_api.register(QuizQuestionResource())
v1_api.register(ResponseResource())
v1_api.register(QuizAttemptResource())

urlpatterns = patterns('',
    url(r'^api/', include(v1_api.urls)),
)
