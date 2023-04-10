from django.contrib.auth.models import User
from django.views.generic import ListView, DetailView

from helpers.mixins.AjaxTemplateResponseMixin import AjaxTemplateResponseMixin
from helpers.mixins.ListItemUrlMixin import ListItemUrlMixin
from oppia.mixins.PermissionMixins import CanViewUserDetailsMixin
from oppia.models import Course, Activity
from quiz.models import QuizAttempt, Quiz


class QuizAttemptsList(CanViewUserDetailsMixin, ListView, ListItemUrlMixin, AjaxTemplateResponseMixin):

    model = QuizAttempt
    objects_url_name = 'quiz_attempt_detail'
    template_name = 'profile/quiz/attempts.html'
    ajax_template_name = 'quiz/attempts_query.html'
    paginate_by = 15
    user_url_kwarg = 'user_id'

    def get_queryset(self):
        user = self.kwargs[self.user_url_kwarg]
        quiz = self.kwargs['quiz_id']

        return QuizAttempt.objects \
            .filter(user__pk=user, quiz__pk=quiz) \
            .order_by('-submitted_date', '-attempt_date')

    def get_context_data(self, **kwargs):

        context = super().get_context_data(**kwargs)
        context['quiz'] = Quiz.objects.get(pk=self.kwargs['quiz_id'])
        context['profile'] = User.objects.get(pk=self.kwargs[self.user_url_kwarg])
        context['course'] = Course.objects.get(pk=self.kwargs['course_id'])

        return context


class UserAttemptsListDetails(CanViewUserDetailsMixin, ListView, ListItemUrlMixin, AjaxTemplateResponseMixin):

    model = QuizAttempt
    objects_url_name = 'quiz_attempt_detail'
    template_name = 'profile/quiz/global_attempts.html'
    ajax_template_name = 'quiz/attempts_query.html'
    paginate_by = 15
    user_url_kwarg = 'user_id'

    def get_queryset(self):
        user = self.kwargs[self.user_url_kwarg]

        quizzes = Quiz.get_by_activity_type(Activity.QUIZ)
        return QuizAttempt.objects \
            .filter(user__pk=user, quiz__in=quizzes) \
            .order_by('-submitted_date', '-attempt_date')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['profile'] = User.objects.get(pk=self.kwargs[self.user_url_kwarg])
        context['show_course_info'] = True
        return context


class QuizAttemptDetail(CanViewUserDetailsMixin, DetailView):

    model = QuizAttempt
    template_name = 'quiz/attempt.html'
    user_url_kwarg = 'user_id'

    def get_queryset(self):
        user = self.kwargs[self.user_url_kwarg]
        quiz = self.kwargs['quiz_id']

        return QuizAttempt.objects \
            .filter(user__pk=user, quiz__pk=quiz) \
            .order_by('-submitted_date', '-attempt_date') \
            .prefetch_related('responses')

    def get_context_data(self, **kwargs):

        context = super().get_context_data(**kwargs)
        context['quiz'] = Quiz.objects.get(pk=self.kwargs['quiz_id'])
        context['profile'] = User.objects.get(pk=self.kwargs['user_id'])
        context['course'] = Course.objects.get(pk=self.kwargs['course_id'])

        return context
