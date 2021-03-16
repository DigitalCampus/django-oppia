from django.contrib.auth.models import User
from django.views.generic import ListView, DetailView

from helpers.mixins.AjaxTemplateResponseMixin import AjaxTemplateResponseMixin
from helpers.mixins.ListItemUrlMixin import ListItemUrlMixin
from oppia.models import Course, Activity
from oppia.permissions import get_user, can_view_course_detail
from quiz.models import QuizAttempt, Quiz


class CourseFeedbackActivitiesList(ListView, ListItemUrlMixin, AjaxTemplateResponseMixin):

    model = Activity
    objects_url_name = 'course_feedback_responses'
    template_name = 'course/feedback.html'
    paginate_by = 15

    def get_queryset(self):
        course = self.kwargs['course_id']
        # check permissions, get_user raises PermissionDenied
        can_view_course_detail(self.request, course)
        return Activity.objects.filter(section__course=course, type=Activity.FEEDBACK)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['course'] = Course.objects.get(pk=self.kwargs['course_id'])
        return context



class CourseFeedbackResponsesList(ListView, ListItemUrlMixin, AjaxTemplateResponseMixin):

    model = QuizAttempt
    objects_url_name = 'profile:feedback_response_detail'
    template_name = 'feedback/responses_list.html'
    ajax_template_name = 'feedback/query.html'
    paginate_by = 15

    def get_queryset(self):
        course = self.kwargs['course_id']
        # check permissions, get_user raises PermissionDenied
        can_view_course_detail(self.request, course)

        activity = Activity.objects.get(pk=self.kwargs['feedback_id'])
        quiz = Quiz.objects.get(quizprops__name='digest',
                                quizprops__value=activity.digest)

        return QuizAttempt.objects.filter(quiz=quiz) \
            .order_by('-submitted_date', '-attempt_date')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['course'] = Course.objects.get(pk=self.kwargs['course_id'])
        context['feedback'] = Activity.objects.get(pk=self.kwargs['feedback_id'])
        context['show_course_info'] = False
        return context


class FeedbackResponseDetail(DetailView):

    model = QuizAttempt
    template_name = 'feedback/response.html'

    def get_queryset(self):
        user = self.kwargs['user_id']
        quiz = self.kwargs['quiz_id']

        # check permissions, get_user raises PermissionDenied
        get_user(self.request, user)

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
