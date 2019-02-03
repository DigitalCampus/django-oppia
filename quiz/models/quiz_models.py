# quiz/models.py
import datetime
from django.apps import apps
from django.contrib.auth.models import User
from django.db import models
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _

from quiz.models import Question

class Quiz(models.Model):
    owner = models.ForeignKey(User, null=True, on_delete=models.SET_NULL)
    created_date = models.DateTimeField('date created', default=timezone.now)
    lastupdated_date = models.DateTimeField('date updated', default=timezone.now)
    draft = models.BooleanField(default=False)
    deleted = models.BooleanField(default=False)
    title = models.TextField(blank=False)
    description = models.TextField(blank=True)
    questions = models.ManyToManyField(Question, through='QuizQuestion')

    class Meta:
        verbose_name = _('Quiz')
        verbose_name_plural = _('Quizzes')

    def __unicode__(self):
        return self.title

    def no_attempts(self):
        no_attempts = QuizAttempt.objects.filter(quiz=self).count()
        return no_attempts

    def avg_score(self):
        # TODO - sure this could be tidied up
        attempts = QuizAttempt.objects.filter(quiz=self)
        total = 0
        for a in attempts:
            total = total + a.get_score_percent()
        if self.no_attempts > 0:
            avg_score = int(total / self.no_attempts())
        else:
            avg_score = 0
        return avg_score

    @staticmethod
    def get_no_attempts_by_user(quiz, user):
        no_attempts = QuizAttempt.objects.filter(quiz=quiz, user=user).count()
        return no_attempts

class QuizQuestion(models.Model):
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    order = models.IntegerField(default=1)

    class Meta:
        verbose_name = _('QuizQuestion')
        verbose_name_plural = _('QuizQuestions')


class QuizProps(models.Model):
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    value = models.TextField(blank=True)

    class Meta:
        verbose_name = _('QuizProp')
        verbose_name_plural = _('QuizProps')

    def __unicode__(self):
        return self.name


class QuizAttempt(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    quiz = models.ForeignKey(Quiz, null=True, default=None, on_delete=models.SET_NULL)
    attempt_date = models.DateTimeField('date attempted', default=timezone.now)
    submitted_date = models.DateTimeField('date submitted', default=timezone.now)
    score = models.DecimalField(decimal_places=2, max_digits=6)
    maxscore = models.DecimalField(decimal_places=2, max_digits=6)
    ip = models.GenericIPAddressField(null=True, blank=True, default=None)
    instance_id = models.CharField(max_length=100, null=True, blank=True, default=None, db_index=True)
    agent = models.TextField(blank=True)
    points = models.IntegerField(blank=True, null=True, default=None)
    event = models.CharField(max_length=50, null=True, blank=True, default=None)

    class Meta:
        verbose_name = _('QuizAttempt')
        verbose_name_plural = _('QuizAttempts')

    def get_score_percent(self):
        if self.maxscore > 0:
            percent = int(round(self.score * 100 / self.maxscore))
        else:
            percent = 0
        return percent

    def is_first_attempt(self):
        no_attempts = QuizAttempt.objects.filter(user=self.user, quiz=self.quiz).count()
        if no_attempts == 1:
            return True
        else:
            return False

    def is_first_attempt_today(self):
        olddate = datetime.datetime.now() + datetime.timedelta(hours=-24)
        no_attempts_today = QuizAttempt.objects.filter(user=self.user, quiz=self.quiz, submitted_date__gte=olddate).count()
        if no_attempts_today == 1:
            return True
        else:
            return False

    def get_quiz_digest(self):
        qp = QuizProps.objects.filter(quiz=self.quiz, name='digest')
        if qp.count() == 1:
            return qp[0].value
        else:
            return None

    def get_tracker(self):
        #get tracker model this way to avoid circular import issues
        tracker = apps.get_model('oppia.tracker')
        trackers = tracker.objects.filter(uuid=self.instance_id)
        if trackers.count() > 0:
            return trackers[0]
        else:
            return None


class QuizAttemptResponse(models.Model):
    quizattempt = models.ForeignKey(QuizAttempt, on_delete=models.CASCADE)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    score = models.DecimalField(decimal_places=2, max_digits=6)
    text = models.TextField(blank=True)

    class Meta:
        verbose_name = _('QuizAttemptResponse')
        verbose_name_plural = _('QuizAttemptResponses')

    def get_score_percent(self):
        if self.question.get_maxscore() > 0:
            percent = int(round(float(self.score) * 100 / self.question.get_maxscore()))
        else:
            percent = 0
        return percent
