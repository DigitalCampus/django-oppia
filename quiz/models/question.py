import json

from django.contrib.auth.models import User
from django.db import models
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _


class Question(models.Model):
    QUESTION_TYPES = (
        ('multichoice', 'Multiple choice'),
        ('shortanswer', 'Short answer'),
        ('matching', 'Matching'),
        ('numerical', 'Numerical'),
        ('multiselect', 'Multiple select'),
        ('description', 'Information only'),
        ('essay', 'Essay question'),
    )
    owner = models.ForeignKey(User, null=True, on_delete=models.SET_NULL)
    created_date = models.DateTimeField('date created', default=timezone.now)
    lastupdated_date = models.DateTimeField('date updated',
                                            default=timezone.now)
    title = models.TextField(blank=False)
    type = models.CharField(max_length=15,
                            choices=QUESTION_TYPES,
                            default='multichoice')

    class Meta:
        verbose_name = _('Question')
        verbose_name_plural = _('Questions')

    def __str__(self):
        return self.title

    def get_maxscore(self):
        props = QuestionProps.objects.get(question=self, name='maxscore')
        return float(props.value)

    def get_title(self, lang='en'):
        try:
            titles = json.loads(self.title)
            if lang in titles:
                return titles[lang]
            else:
                for temp_lang in titles:
                    return titles[temp_lang]
        except json.JSONDecodeError:
            pass
        return self.title

    def get_no_responses(self):
        from quiz.models.quiz_models import QuizAttemptResponse
        return QuizAttemptResponse.objects.filter(
            question=self,
            quizattempt__user__is_staff=False).count()

    def get_difficulty_index(self):
        from quiz.models.quiz_models import QuizAttemptResponse
        qars = QuizAttemptResponse.objects.filter(
            question=self,
            quizattempt__user__is_staff=False)
        total_responses = qars.count()
        total_correct_responses = qars.filter(score__gt=0).count()
        if total_responses > 0:
            return total_correct_responses/total_responses
        else:
            return 0

    def get_discrimination_index(self):
        from quiz.models.quiz_models import QuizAttemptResponse
        qars = QuizAttemptResponse.objects.filter(
            question=self,
            quizattempt__user__is_staff=False).order_by('-score')
        total_count = qars.count()

        top_slice_start = 0
        top_slice_end = int(total_count/(10/3))
        bottom_slice_start = total_count - top_slice_end
        bottom_slice_end = total_count

        top_slice = qars.values_list('id',
                                     flat=True)[top_slice_start:top_slice_end]
        top_slice_ids = [ts for ts in top_slice]
        top_slice_correct = QuizAttemptResponse.objects.filter(
            score__gt=0,
            pk__in=top_slice_ids).count()

        bottom_slice = qars \
            .values_list('id', flat=True)[bottom_slice_start:bottom_slice_end]
        bottom_slice_ids = [bs for bs in bottom_slice]
        bottom_slice_correct = QuizAttemptResponse.objects.filter(
            score__gt=0,
            pk__in=bottom_slice_ids).count()

        if total_count > 0:
            return ((top_slice_correct - bottom_slice_correct)
                    / (top_slice.count() + bottom_slice.count())) * 2 * 100
        else:
            return 0


class QuestionProps(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    value = models.TextField(blank=True)

    class Meta:
        verbose_name = _('QuestionProp')
        verbose_name_plural = _('QuestionProps')

    def __str__(self):
        return self.name
