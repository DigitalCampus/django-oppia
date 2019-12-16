import time
from django.contrib.auth.models import User
from django.views.generic import ListView, DetailView

from helpers.mixins.AjaxTemplateResponseMixin import AjaxTemplateResponseMixin
from helpers.mixins.ListItemUrlMixin import ListItemUrlMixin
from oppia.models import Course
from quiz.models import QuizAttempt, Quiz


class QuizAttemptsList(ListView, ListItemUrlMixin, AjaxTemplateResponseMixin):

    model = QuizAttempt

    objects_url_name = 'profile_user_quiz_attempt_detail'
    template_name = 'profile/quiz/attempts.html'
    ajax_template_name = 'quiz/attempts_query.html'
    paginate_by = 15

    def get_queryset(self):
        user = self.kwargs['user_id']
        quiz = self.kwargs['quiz_id']

        return QuizAttempt.objects.filter(user__pk=user, quiz__pk=quiz)

    def get_context_data(self, **kwargs):

        context = super().get_context_data(**kwargs)
        context['quiz'] = Quiz.objects.get(pk=self.kwargs['quiz_id'])
        context['profile'] = User.objects.get(pk=self.kwargs['user_id'])
        context['course'] = Course.objects.get(pk=self.kwargs['course_id'])

        return context


class UserAttemptsList(ListView, ListItemUrlMixin, AjaxTemplateResponseMixin):

    model = QuizAttempt
    objects_url_name = 'profile_user_quiz_attempt_detail'
    template_name = 'profile/quiz/global_attempts.html'
    ajax_template_name = 'quiz/attempts_query.html'
    paginate_by = 15

    def get_queryset(self):
        user = self.kwargs['user_id']
        return QuizAttempt.objects.filter(user__pk=user)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['profile'] = User.objects.get(pk=self.kwargs['user_id'])
        context['show_course_info'] = True
        return context


class QuizAttemptDetail(DetailView):

    model = QuizAttempt
    template_name = 'quiz/attempt.html'

    def get_queryset(self):
        user = self.kwargs['user_id']
        quiz = self.kwargs['quiz_id']

        return QuizAttempt.objects.filter(user__pk=user, quiz__pk=quiz).prefetch_related('responses')

    def get_context_data(self, **kwargs):

        context = super().get_context_data(**kwargs)
        context['quiz'] = Quiz.objects.get(pk=self.kwargs['quiz_id'])
        context['profile'] = User.objects.get(pk=self.kwargs['user_id'])
        context['course'] = Course.objects.get(pk=self.kwargs['course_id'])

        return context
