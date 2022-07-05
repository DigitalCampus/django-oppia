# oppia/models.py
import datetime
import json
import os

from django.conf import settings
from django.contrib.auth.models import User
from django.db import models
from django.db.models import Max, F, Q
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from tastypie.models import create_api_key

from oppia.models.course_status import CourseStatus
from quiz.models import QuizAttempt, Quiz

from xml.dom.minidom import Document

models.signals.post_save.connect(create_api_key, sender=User)

STR_COURSE_INHERITED = _('Inherited from course')
STR_GLOBAL_INHERITED = _('Inherited from global defaults')


class Course(models.Model):
    user = models.ForeignKey(User, null=True, on_delete=models.CASCADE)
    created_date = models.DateTimeField('date created',
                                        default=timezone.now)
    lastupdated_date = models.DateTimeField('date updated',
                                            default=timezone.now)
    version = models.BigIntegerField()
    title = models.TextField(blank=False)
    description = models.TextField(blank=True,
                                   null=True,
                                   default=None)
    shortname = models.CharField(max_length=200)
    priority = models.IntegerField(default=0)

    filename = models.CharField(max_length=200)
    badge_icon = models.FileField(upload_to="badges",
                                  blank=True,
                                  default=None)

    status = models.ForeignKey('CourseStatus',
                               limit_choices_to=Q(available=True),
                               on_delete=models.PROTECT,
                               null=True,
                               blank=False)

    class Meta:
        verbose_name = _('Course')
        verbose_name_plural = _('Courses')
        ordering = ['title']

    def __str__(self):
        return self.get_title(self)

    def getAbsPath(self):
        return os.path.join(settings.COURSE_UPLOAD_DIR, self.filename)

    def get_title(self, lang='en'):
        try:
            titles = json.loads(self.title)
            if lang in titles:
                return titles[lang]
            else:
                for local_lang in titles:
                    return titles[local_lang]
        except json.JSONDecodeError:
            pass
        return self.title

    def is_first_download(self, user):
        no_downloads = Tracker.objects.filter(user=user, course=self, type='download').count()
        return no_downloads == 0

    def no_downloads(self):
        no_downloads = Tracker.objects.filter(course=self, type='download').count()
        return no_downloads

    def no_distinct_downloads(self):
        no_distinct_downloads = Tracker.objects.filter(course=self, type='download') \
            .values('user_id') \
            .distinct().count()
        return no_distinct_downloads

    def get_activity_today(self):
        return Tracker.objects  \
            .filter(course=self,
                    tracker_date__day=timezone.now().day,
                    tracker_date__month=timezone.now().month,
                    tracker_date__year=timezone.now().year) \
            .count()

    def get_activity_week(self):
        now = timezone.now()
        last_week = timezone.make_aware(
            datetime.datetime(now.year,
                              now.month,
                              now.day) - datetime.timedelta(days=7),
            timezone.get_current_timezone())
        return Tracker.objects.filter(course=self, tracker_date__gte=last_week).count()

    def get_feedback_activities(self):
        return Activity.objects.filter(section__course=self, type=Activity.FEEDBACK)

    def get_quiz_activities(self):
        return Activity.objects.filter(section__course=self, type=Activity.QUIZ)

    def has_quizzes(self):
        return self.get_quiz_activities().exists()

    def has_feedback(self):
        return self.get_feedback_activities().exists()

    def get_removed_quizzes(self):
        current_quizzes = Activity.objects.filter(
            section__course=self,
            type=Activity.QUIZ).values_list('digest', flat=True)
        old_quizzes_digests = Tracker.objects.filter(course=self,
                                                     type=Activity.QUIZ) \
            .exclude(digest__in=current_quizzes).values_list('digest',
                                                             flat=True)
        quizzes = Quiz.objects.filter(quizprops__name='digest',
                                      quizprops__value__in=old_quizzes_digests)
        return quizzes

    def get_removed_feedbacks(self):
        current_quizzes = Activity.objects.filter(
            section__course=self,
            type=Activity.FEEDBACK).values_list('digest', flat=True)
        old_quizzes_digests = Tracker.objects.filter(course=self,
                                                     type=Activity.FEEDBACK) \
            .exclude(digest__in=current_quizzes).values_list('digest',
                                                             flat=True)
        quizzes = Quiz.objects.filter(quizprops__name='digest',
                                      quizprops__value__in=old_quizzes_digests)
        return quizzes

    def get_categories(self):
        from oppia.models import Category
        categories = Category.objects.filter(coursecategory__course=self)
        category_str = ""
        for c in categories:
            category_str = category_str + c.name + ", "
        return category_str[:-2]

    def sections(self):
        sections = Section.objects.filter(course=self).order_by('order')
        return sections

    def get_no_activities(self):
        return Activity.objects.filter(section__course=self,
                                       baseline=False).count()

    def get_no_quizzes(self):
        return Activity.objects.filter(section__course=self,
                                       type=Activity.QUIZ,
                                       baseline=False).count()

    def get_no_media(self):
        return Media.objects.filter(course=self).count()

    def get_no_trackers(self):
        return Tracker.objects.filter(course=self).count()

    @staticmethod
    def get_pre_test_score(course, user):
        try:
            baseline = Activity.objects.get(section__course=course,
                                            type=Activity.QUIZ,
                                            section__order=0)
        except Activity.DoesNotExist:
            return None

        try:
            quiz = Quiz.objects.filter(quizprops__value=baseline.digest,
                                       quizprops__name="digest")
        except Quiz.DoesNotExist:
            return None

        attempts = QuizAttempt.objects.filter(quiz__in=quiz, user=user)
        if attempts.count() != 0:
            max_score = 100 \
                * float(attempts.aggregate(max=Max('score'))['max']) \
                / float(attempts[0].maxscore)
            return max_score
        else:
            return None

    @staticmethod
    def get_no_quizzes_completed(course, user):
        acts = Activity.objects.filter(section__course=course, baseline=False, type=Activity.QUIZ).values_list('digest')
        quizzes = Quiz.objects.filter(quizprops__value__in=acts, quizprops__name="digest")
        quizzes_passed = QuizAttempt.objects \
            .filter(quiz__in=quizzes, user=user)\
            .annotate(percent=F('score')/F('maxscore'))\
            .filter(percent__gte=0.75) \
            .values_list('quiz__id').distinct()
        return quizzes_passed.count()

    @staticmethod
    def get_activities_completed(course, user):
        acts = Activity.objects.filter(section__course=course, baseline=False).values_list('digest')
        return Tracker.objects.filter(course=course, user=user, completed=True, digest__in=acts) \
            .values_list('digest') \
            .distinct() \
            .count()

    @staticmethod
    def get_media_viewed(course, user):
        media = Media.objects.filter(course=course)

        tracker_viewed = Tracker.objects.filter(
            course=course,
            user=user,
            digest__in=media.values_list('digest'),
            completed=True) \
            .values_list('digest') \
            .distinct() \
            .count()

        return tracker_viewed

    def is_live(self):
        return self.status.name == CourseStatus.LIVE

    def is_draft(self):
        return self.status.name == CourseStatus.DRAFT

    def is_archived(self):
        return self.status.name == CourseStatus.ARCHIVED

    def are_new_downloads_disabled(self):
        return self.status.name == CourseStatus.NEW_DOWNLOADS_DISABLED

    def is_read_only(self):
        return self.status.name == CourseStatus.READ_ONLY


class CoursePermissions(models.Model):

    MANAGER = 'manager'
    VIEWER = 'viewer'
    ROLE_TYPES = (
        (MANAGER, 'Manager'),
        (VIEWER, 'Viewer')
    )

    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    role = models.CharField(max_length=20, choices=ROLE_TYPES)

    class Meta:
        verbose_name = _('Course Permission')
        verbose_name_plural = _('Course Permissions')


class Section(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    order = models.IntegerField()
    title = models.TextField(blank=False)

    class Meta:
        verbose_name = _('Section')
        verbose_name_plural = _('Sections')

    def __str__(self):
        return self.get_title()

    def get_title(self, lang='en'):
        try:
            titles = json.loads(self.title)
            if lang in titles:
                return titles[lang]
            else:
                for local_lang in titles:
                    return titles[local_lang]
        except json.JSONDecodeError:
            pass
        return self.title

    def activities(self):
        activities = Activity.objects.filter(section=self).order_by('order')
        return activities


class Activity(models.Model):
    QUIZ = 'quiz'
    MEDIA = 'media'
    PAGE = 'page'
    FEEDBACK = 'feedback'
    ACTIVITY_TYPES = (
        (QUIZ, 'Quiz'),
        (MEDIA, 'Media'),
        (PAGE, 'Page'),
        (FEEDBACK, 'Feedback')
    )

    section = models.ForeignKey(Section, on_delete=models.CASCADE)
    order = models.IntegerField(default=0)
    title = models.TextField(blank=False)
    type = models.CharField(max_length=10)
    digest = models.CharField(max_length=100)
    baseline = models.BooleanField(default=False)
    image = models.TextField(blank=True, null=True, default=None)
    content = models.TextField(blank=True, null=True, default=None)
    description = models.TextField(blank=True, null=True, default=None)

    def __str__(self):
        return self.get_title()

    class Meta:
        verbose_name = _('Activity')
        verbose_name_plural = _('Activities')

    def get_title(self, lang='en'):
        try:
            titles = json.loads(self.title)
            if lang in titles:
                return titles[lang]
            else:
                for local_lang in titles:
                    return titles[local_lang]
        except json.JSONDecodeError:
            pass
        return self.title

    def get_content(self, lang='en'):
        try:
            contents = json.loads(self.content)
            if lang in contents:
                return contents[lang]
            else:
                for local_lang in contents:
                    return contents[local_lang]
        except json.JSONDecodeError:
            pass
        return self.content

    def get_next_activity(self):
        try:
            next_activity = Activity.objects \
                                .get(section__course=self.section.course,
                                     order=self.order + 1,
                                     section=self.section)
        except Activity.DoesNotExist:
            try:
                next_activity = Activity.objects.get(
                                    section__course=self.section.course,
                                    section__order=self.section.order + 1,
                                    order=1)
            except Activity.DoesNotExist:
                next_activity = None
        return next_activity

    def get_previous_activity(self):
        try:
            prev_activity = Activity.objects.get(
                                section__course=self.section.course,
                                order=self.order - 1,
                                section=self.section)
        except Activity.DoesNotExist:
            try:
                max_order = Activity.objects \
                              .filter(section__course=self.section.course,
                                      section__order=self.section.order - 1) \
                              .aggregate(max_order=Max('order'))
                prev_activity = Activity.objects.get(
                                    section__course=self.section.course,
                                    section__order=self.section.order - 1,
                                    order=max_order['max_order'])
            except Activity.DoesNotExist:
                prev_activity = None
        return prev_activity

    def get_event_points(self):
        from gamification.models import DefaultGamificationEvent, \
                                        CourseGamificationEvent, \
                                        ActivityGamificationEvent
        event_points = []

        # first check if there are specific points for this activity
        activity_custom_points = ActivityGamificationEvent.objects \
            .filter(activity=self)
        if len(activity_custom_points) > 0:
            source = _('Custom Points')
            return {'events': activity_custom_points, 'source': source}

        # if not, then check the points for the course as a whole or then the
        # global default points
        if self.type == self.PAGE:
            course_custom_points = CourseGamificationEvent.objects \
                .filter(course__section__activity=self,
                        event__startswith='activity_')

            if len(course_custom_points) > 0:
                source = STR_COURSE_INHERITED
                return {'events': course_custom_points, 'source': source}
            else:
                default_activity_events = DefaultGamificationEvent.objects \
                    .filter(level=DefaultGamificationEvent.ACTIVITY)
                source = STR_COURSE_INHERITED
                return {'events': default_activity_events, 'source': source}

        if self.type == self.QUIZ:
            course_custom_points = CourseGamificationEvent.objects \
                .filter(course__section__activity=self,
                        event__startswith='quiz_')
            if len(course_custom_points) > 0:
                source = STR_COURSE_INHERITED
                return {'events': course_custom_points, 'source': source}
            else:
                default_quiz_events = DefaultGamificationEvent.objects \
                    .filter(level=DefaultGamificationEvent.QUIZ)
                source = STR_GLOBAL_INHERITED
                return {'events': default_quiz_events, 'source': source}

        return event_points

    def get_no_quiz_responses(self):
        # get the actual quiz id
        quiz = Quiz.objects.filter(quizprops__name='digest',
                                   quizprops__value=self.digest).last()
        return QuizAttempt.objects.filter(
            quiz_id=quiz.id).count() if quiz is not None else 0


class Media(models.Model):
    URL_MAX_LENGTH = 250

    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    digest = models.CharField(max_length=100)
    filename = models.CharField(max_length=200)
    download_url = models.URLField(max_length=URL_MAX_LENGTH)
    filesize = models.BigIntegerField(default=None, blank=True, null=True)
    media_length = models.IntegerField(default=None, blank=True, null=True)

    class Meta:
        verbose_name = _('Media')
        verbose_name_plural = _('Media')

    def __str__(self):
        return self.filename

    def get_event_points(self):
        from gamification.models import DefaultGamificationEvent, \
                                        CourseGamificationEvent, \
                                        MediaGamificationEvent

        # first check if there are specific points for this activity
        media_custom_points = MediaGamificationEvent.objects \
            .filter(media=self)
        if media_custom_points.exists():
            source = _('Custom Points')
            return {'events': media_custom_points, 'source': source}

        # if not, then check the points for the course as a whole or then
        # the global default points
        course_custom_points = CourseGamificationEvent.objects \
            .filter(course=self.course,
                    event__startswith='media_')

        if course_custom_points.exists():
            source = STR_COURSE_INHERITED
            return {'events': course_custom_points, 'source': source}
        else:
            default_media_events = DefaultGamificationEvent.objects \
                .filter(level=DefaultGamificationEvent.MEDIA)
            source = STR_GLOBAL_INHERITED
            return {'events': default_media_events, 'source': source}


class Tracker(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    submitted_date = models.DateTimeField('date submitted',
                                          default=timezone.now,
                                          db_index=True)
    tracker_date = models.DateTimeField('date tracked',
                                        default=timezone.now,
                                        db_index=True)
    ip = models.GenericIPAddressField(null=True, blank=True, default=None)
    agent = models.TextField(blank=True)
    digest = models.CharField(max_length=100)
    data = models.TextField(blank=True)
    course = models.ForeignKey(Course,
                               null=True,
                               blank=True,
                               default=None,
                               on_delete=models.SET_NULL)
    type = models.CharField(max_length=10,
                            null=True,
                            blank=True,
                            default=None)
    completed = models.BooleanField(default=False)
    time_taken = models.IntegerField(default=0)
    course_version = models.BigIntegerField(null=True, blank=True)
    activity_title = models.TextField(blank=True,
                                      null=True,
                                      default=None)
    section_title = models.TextField(blank=True,
                                     null=True,
                                     default=None)
    uuid = models.CharField(max_length=100,
                            blank=True,
                            null=True,
                            default=None,
                            db_index=True)
    lang = models.CharField(max_length=10,
                            null=True,
                            blank=True,
                            default=None)
    points = models.IntegerField(blank=True,
                                 null=True,
                                 default=None)
    event = models.CharField(max_length=50,
                             null=True,
                             blank=True,
                             default=None)

    class Meta:
        verbose_name = _('Tracker')
        verbose_name_plural = _('Trackers')
        indexes = [models.Index(fields=['course', 'user']), ]

    def __str__(self):
        return self.agent

    def is_first_tracker_today(self):
        olddate = timezone.now() + datetime.timedelta(hours=-24)
        no_attempts_today = Tracker.objects \
            .filter(user=self.user,
                    digest=self.digest,
                    completed=True,
                    submitted_date__gte=olddate) \
            .count()
        if no_attempts_today == 1:
            return True
        else:
            return False

    def get_activity_type(self):
        activities = Activity.objects.filter(digest=self.digest)
        for a in activities:
            return a.type
        media = Media.objects.filter(digest=self.digest)
        if media.exists():
            return "media"
        return None

    def get_media_title(self):
        media = Media.objects.filter(digest=self.digest)
        for m in media:
            return m.filename
        return None

    def get_activity_title(self, lang='en'):
        media = Media.objects.filter(digest=self.digest)
        for m in media:
            return m.filename
        try:
            activity = Activity.objects.filter(digest=self.digest)
            for a in activity:
                titles = json.loads(a.title)
                if lang in titles:
                    return titles[lang]
                else:
                    for local_lang in titles:
                        return titles[local_lang]
        except TypeError:
            pass
        return self.activity_title

    def get_section_title(self, lang='en'):
        try:
            titles = json.loads(self.section_title)
            if lang in titles:
                return titles[lang]
            else:
                for local_lang in titles:
                    return titles[local_lang]
        except TypeError:
            pass
        return self.section_title

    def activity_exists(self):
        activities = Activity.objects.filter(digest=self.digest)
        if activities.exists():
            return True
        media = Media.objects.filter(digest=self.digest)
        if media.exists():
            return True
        return False

    @staticmethod
    def has_completed_trackers(course, user):
        return Tracker.objects.filter(user=user, course=course, completed=True).exists()

    @staticmethod
    def to_xml_string(course, user):
        doc = Document()
        tracker_xml = doc.createElement('trackers')
        doc.appendChild(tracker_xml)
        trackers = Tracker.objects.filter(user=user, course=course)
        for t in trackers:
            track = doc.createElement('tracker')
            track.setAttribute('digest', t.digest)
            track.setAttribute('submitteddate',
                               t.submitted_date.strftime('%Y-%m-%d %H:%M:%S'))
            track.setAttribute('completed', str(t.completed))
            track.setAttribute('type', t.type)
            track.setAttribute('event', t.event)
            track.setAttribute('points', str(t.points))
            if t.type == 'quiz':
                try:
                    quiz = doc.createElement('quiz')
                    data = json.loads(t.data)
                    quiz_attempt = QuizAttempt.objects \
                        .filter(instance_id=data['instance_id'],
                                user=user) \
                        .order_by('-submitted_date').first()
                    if quiz_attempt:
                        quiz.setAttribute('score', str(quiz_attempt.score))
                        quiz.setAttribute('maxscore',
                                          str(quiz_attempt.maxscore))
                        quiz.setAttribute('submitteddate',
                                          quiz_attempt
                                          .submitted_date
                                          .strftime('%Y-%m-%d %H:%M:%S'))
                        quiz.setAttribute('passed', str(t.completed))
                        quiz.setAttribute("course", course.shortname)
                        quiz.setAttribute("event", quiz_attempt.event)
                        quiz.setAttribute("points", str(quiz_attempt.points))
                        quiz.setAttribute("timetaken",
                                          str(quiz_attempt.time_taken))
                        track.appendChild(quiz)
                except QuizAttempt.DoesNotExist:
                    pass
                except json.JSONDecodeError:
                    pass
            tracker_xml.appendChild(track)
        return doc.toxml()

    @staticmethod
    def activity_views(user,
                       type,
                       start_date=None,
                       end_date=None,
                       course=None):
        results = Tracker.objects.filter(user=user, type=type)
        if start_date:
            results = results.filter(submitted_date__gte=start_date)
        if end_date:
            results = results.filter(submitted_date__lte=end_date)
        if course:
            results = results.filter(course=course)
        return results.count()

    def get_lang(self):
        try:
            json_data = json.loads(self.data)
        except ValueError:
            return None

        if 'lang' in json_data:
            return json_data['lang']
