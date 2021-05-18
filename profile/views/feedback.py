from django.contrib.auth.models import User
from django.views.generic import ListView

from helpers.mixins.AjaxTemplateResponseMixin import AjaxTemplateResponseMixin
from helpers.mixins.ListItemUrlMixin import ListItemUrlMixin
from oppia.models import Course, Activity
from oppia.permissions import get_user
from quiz.models import QuizAttempt, Quiz


class FeedbackAttemptsList(ListView,
                           ListItemUrlMixin,
                           AjaxTemplateResponseMixin):

    model = QuizAttempt

    objects_url_name = 'quiz_attempt_detail'
    template_name = 'profile/quiz/attempts.html'
    ajax_template_name = 'quiz/attempts_query.html'
    paginate_by = 15

    def get_queryset(self):
        user = self.kwargs['user_id']
        quiz = self.kwargs['quiz_id']

        # check permissions, get_user raises PermissionDenied
        get_user(self.request, user)

        return QuizAttempt.objects \
            .filter(user__pk=user, quiz__pk=quiz) \
            .order_by('-submitted_date', '-attempt_date')

    def get_context_data(self, **kwargs):

        context = super().get_context_data(**kwargs)
        context['quiz'] = Quiz.objects.get(pk=self.kwargs['quiz_id'])
        context['profile'] = User.objects.get(pk=self.kwargs['user_id'])
        context['course'] = Course.objects.get(pk=self.kwargs['course_id'])

        return context


class UserFeedbackResponsesList(ListView,
                                ListItemUrlMixin,
                                AjaxTemplateResponseMixin):

    model = QuizAttempt
    objects_url_name = 'oppia:feedback_response_detail'
    template_name = 'profile/feedback/global_responses.html'
    ajax_template_name = 'feedback/query.html'
    paginate_by = 15

    def get_queryset(self):
        user = self.kwargs['user_id']

        # check permissions, get_user raises PermissionDenied
        get_user(self.request, user)

        quizzes = Quiz.get_by_activity_type(Activity.FEEDBACK)
        return QuizAttempt.objects \
            .filter(user__pk=user, quiz__in=quizzes) \
            .order_by('-submitted_date', '-attempt_date')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['profile'] = User.objects.get(pk=self.kwargs['user_id'])
        context['show_course_info'] = True
        return context
