from django.contrib.auth.models import User
from django.views.generic import ListView

from oppia.models import Course
from quiz.models import QuizAttempt, Quiz


class QuizAttemptsList(ListView):

    model = QuizAttempt

    objects_url_name = 'consumer_detail'
    template_name = 'profile/quiz_attempts.html'
    ajax_template_name = 'quiz_attempt/query.html'
    paginate_by = 15

    def get_queryset(self):
        user = self.kwargs['user_id']
        quiz = self.kwargs['quiz_id']
        queryset = QuizAttempt.objects.filter(user__pk=user, quiz__pk=quiz)

        return queryset

    def get_context_data(self, **kwargs):

        context = super().get_context_data(**kwargs)
        context['quiz'] = Quiz.objects.get(pk=self.kwargs['quiz_id'])
        context['profile'] = User.objects.get(pk=self.kwargs['user_id'])
        context['course'] = Course.objects.get(pk=self.kwargs['course_id'])

        return context

