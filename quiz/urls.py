# oppia/quiz/urls.py
from django.conf.urls import include, url

from tastypie.api import Api

from quiz.api.resources import QuizResource, QuizPropsResource, QuestionResource, QuizQuestionResource, \
    ResponseResource, QuizAttemptResource


def get_api(version_name):
    api = Api(api_name=version_name)
    api.register(QuizResource())
    api.register(QuizPropsResource())
    api.register(QuestionResource())
    api.register(QuizQuestionResource())
    api.register(ResponseResource())
    api.register(QuizAttemptResource())

    return api


urlpatterns = [
    url(r'^api/', include(get_api('v1').urls)),

]