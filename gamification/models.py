# oppia/gamification/models.py
from django.contrib.auth.models import User
from django.db import models
from django.utils.translation import gettext_lazy as _
from django.utils import timezone

from oppia.models import Course, Activity, Media


class DefaultGamificationEvent(models.Model):
    GLOBAL = 'global'
    COURSE = 'course'
    ACTIVITY = 'activity'
    QUIZ = 'quiz'
    MEDIA = 'media'
    LEVELS = (
        (GLOBAL, 'Global'),
        (COURSE, 'Course'),
        (ACTIVITY, 'Activity'),
        (QUIZ, 'Quiz'),
        (MEDIA, 'Media')
    )

    event = models.CharField(max_length=100)
    points = models.IntegerField()
    level = models.CharField(max_length=20, choices=LEVELS)
    label = models.CharField(max_length=100)
    helper_text = models.TextField(null=True, default=None)

    class Meta:
        verbose_name = _(u'Default Gamification Event')
        verbose_name_plural = _(u'Default Gamification Events')

    def __str__(self):
        return self.event


class GamificationEvent(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created_date = models.DateTimeField('date created', default=timezone.now)
    event = models.CharField(max_length=100)
    points = models.IntegerField()

    class Meta:
        abstract = True

    def __init__(self, *args, **kwargs):
        super(GamificationEvent, self).__init__(*args, **kwargs)
        self.__default_event = None

    def __str__(self):
        return self.event

    @property
    def default_event(self):
        if not self.__default_event:
            self.__default_event = DefaultGamificationEvent.objects \
                .get(event=self.event)
        return self.__default_event

    def get_label(self):
        return self.default_event.label

    def get_helper_text(self):
        return self.default_event.helper_text


class CourseGamificationEvent(GamificationEvent):
    course = models.ForeignKey(Course,
                               on_delete=models.CASCADE,
                               related_name='gamification_events')

    class Meta:
        verbose_name = _(u'Course Gamification Event')
        verbose_name_plural = _(u'Course Gamification Events')


class ActivityGamificationEvent(GamificationEvent):
    activity = models.ForeignKey(Activity,
                                 on_delete=models.CASCADE,
                                 related_name='gamification_events')

    class Meta:
        verbose_name = _(u'Activity Gamification Event')
        verbose_name_plural = _(u'Activity Gamification Events')


class MediaGamificationEvent(GamificationEvent):
    media = models.ForeignKey(Media,
                              on_delete=models.CASCADE,
                              related_name='gamification_events')

    class Meta:
        verbose_name = _(u'Media Gamification Event')
        verbose_name_plural = _(u'Media Gamification Events')
