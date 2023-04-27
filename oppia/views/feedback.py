from django.http import HttpResponseRedirect
from django.urls import reverse
from django.utils.decorators import method_decorator
from django.views.generic import ListView, DetailView

from helpers.mixins.AjaxTemplateResponseMixin import AjaxTemplateResponseMixin
from helpers.mixins.ListItemUrlMixin import ListItemUrlMixin
from oppia.models import Course, Activity
from oppia.permissions import permission_view_course_detail
from quiz.models import QuizAttempt, Quiz, QuizProps


@method_decorator(permission_view_course_detail, name='dispatch')
class CourseFeedbackActivitiesList(ListView,
                                   ListItemUrlMixin,
                                   AjaxTemplateResponseMixin):

    model = Activity
    objects_url_name = 'course_feedback_responses'
    template_name = 'course/feedback.html'
    paginate_by = 15

    def get_queryset(self):
        course = self.kwargs['course_id']
        return Activity.objects.filter(section__course=course, type=Activity.FEEDBACK)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['course'] = Course.objects.get(pk=self.kwargs['course_id'])
        return context

    def get(self, request, *args, **kwargs):
        feedbacks = self.get_queryset()
        if feedbacks.count() == 1:
            # If there is only one feedback activity, we can
            feedback = feedbacks[0]
            return HttpResponseRedirect(
                reverse('oppia:course_feedback_responses',
                        kwargs={'course_id': self.kwargs['course_id'],
                                'feedback_id': feedback.id}))

        return super().get(request, *args, **kwargs)


@method_decorator(permission_view_course_detail, name='dispatch')
class CourseFeedbackResponsesList(ListView, ListItemUrlMixin, AjaxTemplateResponseMixin):

    model = QuizAttempt
    objects_url_name = 'feedback_response_detail'
    template_name = 'feedback/responses_list.html'
    ajax_template_name = 'feedback/query.html'
    paginate_by = 15

    def get_queryset(self):
        activity = Activity.objects.get(pk=self.kwargs['feedback_id'])
        quiz = Quiz.objects.filter(quizprops__name=QuizProps.DIGEST,
                                   quizprops__value=activity.digest).last()

        return QuizAttempt.objects.filter(quiz=quiz) \
            .order_by('-submitted_date', '-attempt_date')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['course'] = Course.objects.get(pk=self.kwargs['course_id'])
        context['feedback'] = Activity.objects.get(
            pk=self.kwargs['feedback_id'])
        context['show_course_info'] = False
        return context


class FeedbackResponseDetail(DetailView):

    model = QuizAttempt
    template_name = 'feedback/response.html'

    def get_context_data(self, **kwargs):

        context = super().get_context_data(**kwargs)
        context['quiz'] = Quiz.objects.get(pk=self.kwargs['quiz_id'])
        context['profile'] = self.object.user
        context['course'] = Course.objects.get(pk=self.kwargs['course_id'])

        return context
