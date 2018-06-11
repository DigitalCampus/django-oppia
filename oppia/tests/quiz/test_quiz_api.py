# coding: utf-8

# oppia/tests/quiz/test_quiz_api.py
from django.contrib.auth.models import User
from django.test import TestCase
from django.test.client import Client

from oppia.models import Tracker
from oppia.quiz.models import QuizAttempt, QuizAttemptResponse

from tastypie.test import ResourceTestCaseMixin



# TODO QuizQuestionResource
# TODO QuestionResource
# TODO QuestionPropsResource
# TODO ResponseResource
# TODO ResponsePropsResource
# TODO QuizPropsResource
    # getting a quiz via digest

# TODO QuizResource
    # TODO check get and post valid
    # getting a quiz via id no

    # getting an invalid digest
    # creating a quiz (and data required etc)
