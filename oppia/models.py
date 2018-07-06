# oppia/models.py
import datetime
import json

from django.conf import settings
from django.contrib.auth.models import User
from django.db import models
from django.db.models import Max, Sum, Q, F, Count
from django.utils.translation import ugettext_lazy as _
from django.utils import timezone

from oppia.quiz.models import Quiz, QuizAttempt

from tastypie.models import create_api_key

from xml.dom.minidom import *

models.signals.post_save.connect(create_api_key, sender=User)


class Course(models.Model):
    user = models.ForeignKey(User, null=True, on_delete=models.CASCADE)
    created_date = models.DateTimeField('date created', default=timezone.now)
    lastupdated_date = models.DateTimeField('date updated', default=timezone.now)
    version = models.BigIntegerField()
    title = models.TextField(blank=False)
    description = models.TextField(blank=True, null=True, default=None)
    shortname = models.CharField(max_length=200)
    filename = models.CharField(max_length=200)
    badge_icon = models.FileField(upload_to="badges", blank=True, default=None)
    is_draft = models.BooleanField(default=False)
    is_archived = models.BooleanField(default=False)

    class Meta:
        verbose_name = _('Course')
        verbose_name_plural = _('Courses')

    def __unicode__(self):
        return self.get_title(self)

    def getAbsPath(self):
        return settings.COURSE_UPLOAD_DIR + self.filename

    def get_title(self, lang='en'):
        try:
            titles = json.loads(self.title)
            if lang in titles:
                return titles[lang]
            else:
                for l in titles:
                    return titles[l]
        except:
            pass
        return self.title

    def is_first_download(self, user):
        no_attempts = Tracker.objects.filter(user=user, course=self, type='download').count()
        is_first_download = False
        if no_attempts == 1:
            is_first_download = True
        return is_first_download

    def no_downloads(self):
        no_downloads = Tracker.objects.filter(course=self, type='download').count()
        return no_downloads

    def no_distinct_downloads(self):
        no_distinct_downloads = Tracker.objects.filter(course=self, type='download').values('user_id').distinct().count()
        return no_distinct_downloads

    def get_activity_today(self):
        return Tracker.objects.filter(course=self,
                                      tracker_date__day=timezone.now().day,
                                      tracker_date__month=timezone.now().month,
                                      tracker_date__year=timezone.now().year).count()

    def get_activity_week(self):
        now = datetime.datetime.now()
        last_week = datetime.datetime(now.year, now.month, now.day) - datetime.timedelta(days=7)
        return Tracker.objects.filter(course=self,
                                      tracker_date__gte=last_week).count()

    def has_quizzes(self):
        quiz_count = Activity.objects.filter(section__course=self, type=Activity.QUIZ).count()
        if quiz_count > 0:
            return True
        else:
            return False

    def has_feedback(self):
        fb_count = Activity.objects.filter(section__course=self, type='feedback').count()
        if fb_count > 0:
            return True
        else:
            return False

    def get_tags(self):
        tags = Tag.objects.filter(coursetag__course=self)
        str = ""
        for t in tags:
            str = str + t.name + ", "
        return str[:-2]

    def sections(self):
        sections = Section.objects.filter(course=self).order_by('order')
        return sections

    def get_no_activities(self):
        return Activity.objects.filter(section__course=self, baseline=False).count()

    def get_no_quizzes(self):
        return Activity.objects.filter(section__course=self, type=Activity.QUIZ, baseline=False).count()

    def get_no_media(self):
        return Media.objects.filter(course=self).count()

    @staticmethod
    def get_pre_test_score(course, user):
        try:
            baseline = Activity.objects.get(section__course=course, type=Activity.QUIZ, section__order=0)
        except Activity.DoesNotExist:
            return None

        try:
            quiz = Quiz.objects.filter(quizprops__value=baseline.digest, quizprops__name="digest")
        except Quiz.DoesNotExist:
            return None

        attempts = QuizAttempt.objects.filter(quiz__in=quiz, user=user)
        if attempts.count() != 0:
            max_score = 100 * float(attempts.aggregate(max=Max('score'))['max']) / float(attempts[0].maxscore)
            return max_score
        else:
            return None

    @staticmethod
    def get_no_quizzes_completed(course, user):
        acts = Activity.objects.filter(section__course=course, baseline=False, type=Activity.QUIZ).values_list('digest')
        return Tracker.objects.filter(course=course, user=user, completed=True, digest__in=acts).values_list('digest').distinct().count()

    @staticmethod
    def get_activities_completed(course, user):
        acts = Activity.objects.filter(section__course=course, baseline=False).values_list('digest')
        return Tracker.objects.filter(course=course, user=user, completed=True, digest__in=acts).values_list('digest').distinct().count()

    @staticmethod
    def get_points(course, user):
        points = Points.objects.filter(course=course, user=user).aggregate(total=Sum('points'))
        return points['total']

    @staticmethod
    def get_badges(course, user):
        return Award.objects.filter(user=user, awardcourse__course=course).count()

    @staticmethod
    def get_media_viewed(course, user):
        acts = Media.objects.filter(course=course).values_list('digest')
        return Tracker.objects.filter(course=course, user=user, digest__in=acts).values_list('digest').distinct().count()

        
class CourseManager(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    class Meta:
        verbose_name = _('Course Manager')
        verbose_name_plural = _('Course Managers')


class Tag(models.Model):
    name = models.TextField(blank=False)
    created_date = models.DateTimeField('date created', default=timezone.now)
    created_by = models.ForeignKey(User, null=True, on_delete=models.SET_NULL)
    courses = models.ManyToManyField(Course, through='CourseTag')
    description = models.TextField(blank=True, null=True, default=None)
    order_priority = models.IntegerField(default=0)
    highlight = models.BooleanField(default=False)
    icon = models.FileField(upload_to="tags", null=True, blank=True, default=None)

    class Meta:
        verbose_name = _('Tag')
        verbose_name_plural = _('Tags')

    def __unicode__(self):
        return self.name


class CourseTag(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    tag = models.ForeignKey(Tag, on_delete=models.CASCADE)

    class Meta:
        verbose_name = _('Course Tag')
        verbose_name_plural = _('Course Tags')


class Section(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    order = models.IntegerField()
    title = models.TextField(blank=False)

    class Meta:
        verbose_name = _('Section')
        verbose_name_plural = _('Sections')

    def __unicode__(self):
        return self.get_title()

    def get_title(self, lang='en'):
        try:
            titles = json.loads(self.title)
            if lang in titles:
                return titles[lang]
            else:
                for l in titles:
                    return titles[l]
        except:
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
    order = models.IntegerField()
    title = models.TextField(blank=False)
    type = models.CharField(max_length=10)
    digest = models.CharField(max_length=100)
    baseline = models.BooleanField(default=False)
    image = models.TextField(blank=True, null=True, default=None)
    content = models.TextField(blank=True, null=True, default=None)
    description = models.TextField(blank=True, null=True, default=None)

    def __unicode__(self):
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
                for l in titles:
                    return titles[l]
        except:
            pass
        return self.title

    def get_content(self, lang='en'):
        try:
            contents = json.loads(self.content)
            if lang in contents:
                return contents[lang]
            else:
                for l in contents:
                    return contents[l]
        except:
            pass
        return self.content

    def get_next_activity(self):
        try:
            next_activity = Activity.objects.get(section__course=self.section.course, order=self.order + 1, section=self.section)
        except Activity.DoesNotExist:
            try:
                next_activity = Activity.objects.get(section__course=self.section.course, section__order=self.section.order + 1, order=1)
            except Activity.DoesNotExist:
                next_activity = None
        return next_activity

    def get_previous_activity(self):
        try:
            prev_activity = Activity.objects.get(section__course=self.section.course, order=self.order - 1, section=self.section)
        except Activity.DoesNotExist:
            try:
                max_order = Activity.objects.filter(section__course=self.section.course, section__order=self.section.order - 1).aggregate(max_order=Max('order'))
                prev_activity = Activity.objects.get(section__course=self.section.course, section__order=self.section.order - 1, order=max_order['max_order'])
            except:
                prev_activity = None
        return prev_activity


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

    def __unicode__(self):
        return self.filename


class Tracker(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    submitted_date = models.DateTimeField('date submitted', default=timezone.now)
    tracker_date = models.DateTimeField('date tracked', default=timezone.now)
    ip = models.GenericIPAddressField(null=True, blank=True, default=None)
    agent = models.TextField(blank=True)
    digest = models.CharField(max_length=100)
    data = models.TextField(blank=True)
    course = models.ForeignKey(Course, null=True, blank=True, default=None, on_delete=models.SET_NULL)
    type = models.CharField(max_length=10, null=True, blank=True, default=None)
    completed = models.BooleanField(default=False)
    time_taken = models.IntegerField(default=0)
    activity_title = models.TextField(blank=True, null=True, default=None)
    section_title = models.TextField(blank=True, null=True, default=None)
    uuid = models.CharField(max_length=100, blank=True, null=True, default=None, db_index=True)
    lang = models.CharField(max_length=10, null=True, blank=True, default=None)
    points = models.IntegerField(blank=True, null=True, default=None)
    event = models.CharField(max_length=50, null=True, blank=True, default=None)

    class Meta:
        verbose_name = _('Tracker')
        verbose_name_plural = _('Trackers')

    def __unicode__(self):
        return self.agent

    def is_first_tracker_today(self):
        olddate = timezone.now() + datetime.timedelta(hours=-24)
        no_attempts_today = Tracker.objects.filter(user=self.user, digest=self.digest, completed=True, submitted_date__gte=olddate).count()
        if no_attempts_today == 1:
            return True
        else:
            return False

    def get_activity_type(self):
        activities = Activity.objects.filter(digest=self.digest)
        for a in activities:
            return a.type
        media = Media.objects.filter(digest=self.digest)
        for m in media:
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
                    for l in titles:
                        return titles[l]
        except:
            pass
        return self.activity_title

    def get_section_title(self, lang='en'):
        try:
            titles = json.loads(self.section_title)
            if lang in titles:
                return titles[lang]
            else:
                for l in titles:
                    return titles[l]
        except:
            pass
        return self.section_title

    def activity_exists(self):
        activities = Activity.objects.filter(digest=self.digest).count()
        if activities >= 1:
            return True
        media = Media.objects.filter(digest=self.digest).count()
        if media >= 1:
            return True
        return False

    @staticmethod
    def has_completed_trackers(course, user):
        count = Tracker.objects.filter(user=user, course=course, completed=True).count()
        if count > 0:
            return True
        return False

    @staticmethod
    def to_xml_string(course, user):
        doc = Document()
        tracker_xml = doc.createElement('trackers')
        doc.appendChild(tracker_xml)
        trackers = Tracker.objects.filter(user=user, course=course)
        for t in trackers:
            track = doc.createElement('tracker')
            track.setAttribute('digest', t.digest)
            track.setAttribute('submitteddate', t.submitted_date.strftime('%Y-%m-%d %H:%M:%S'))
            track.setAttribute('completed', str(t.completed))
            track.setAttribute('type', t.type)
            track.setAttribute('event', t.event)
            track.setAttribute('points', t.points)
            if t.type == 'quiz':
                try:
                    quiz = doc.createElement('quiz')
                    data = json.loads(t.data)
                    quiz_attempt = QuizAttempt.objects.filter(instance_id=data['instance_id'], user=user).order_by('-submitted_date')[:1]
                    quiz.setAttribute('score', str(quiz_attempt[0].score))
                    quiz.setAttribute('maxscore', str(quiz_attempt[0].maxscore))
                    quiz.setAttribute('submitteddate', quiz_attempt[0].submitted_date.strftime('%Y-%m-%d %H:%M:%S'))
                    quiz.setAttribute('passed', str(t.completed))
                    quiz.setAttribute("course", course.shortname)
                    quiz.setAttribute("event", quiz_attempt[0].event)
                    quiz.setAttribute("points", quiz_attempt[0].points)
                    track.appendChild(quiz)
                except ValueError:
                    pass
                except IndexError:
                    pass
            tracker_xml.appendChild(track)
        return doc.toxml()

    @staticmethod
    def activity_views(user, type, start_date=None, end_date=None, course=None):
        results = Tracker.objects.filter(user=user, type=type)
        if start_date:
            results = results.filter(submitted_date__gte=start_date)
        if end_date:
            results = results.filter(submitted_date__lte=end_date)
        if course:
            results = results.filter(course=course)
        return results.count()

    @staticmethod
    def activity_secs(user, type, start_date=None, end_date=None, course=None):
        results = Tracker.objects.filter(user=user, type=type)
        if start_date:
            results = results.filter(submitted_date__gte=start_date)
        if end_date:
            results = results.filter(submitted_date__lte=end_date)
        if course:
            results = results.filter(course=course)
        time = results.aggregate(total=Sum('time_taken'))
        if time['total'] is None:
            return 0
        return time['total']

    def get_lang(self):
        try:
            json_data = json.loads(self.data)
        except ValueError:
            return None

        if 'lang' in json_data:
            return json_data['lang']

 
class Cohort(models.Model):
    description = models.CharField(max_length=100)
    start_date = models.DateTimeField(default=timezone.now)
    end_date = models.DateTimeField(default=timezone.now)

    class Meta:
        verbose_name = _('Cohort')
        verbose_name_plural = _('Cohorts')

    def __unicode__(self):
        return self.description

    def no_student_members(self):
        return Participant.objects.filter(cohort=self, role=Participant.STUDENT).count()

    def no_teacher_members(self):
        return Participant.objects.filter(cohort=self, role=Participant.TEACHER).count()
    
    @staticmethod
    def student_member_now(course, user):
        now = timezone.now()
        cohorts = Cohort.objects.filter(coursecohort__course=course, start_date__lte=now, end_date__gte=now)
        for c in cohorts:
            participants = c.participant_set.filter(user=user, role=Participant.STUDENT)
            for p in participants:
                return c
        return None

    @staticmethod
    def teacher_member_now(course, user):
        now = timezone.now()
        cohorts = Cohort.objects.filter(coursecohort__course=course, start_date__lte=now, end_date__gte=now)
        for c in cohorts:
            participants = c.participant_set.filter(user=user, role=Participant.TEACHER)
            for p in participants:
                return c
        return None

    @staticmethod
    def member_now(course, user):
        now = timezone.now()
        cohorts = Cohort.objects.filter(coursecohort__course=course, start_date__lte=now, end_date__gte=now)
        for c in cohorts:
            participants = c.participant_set.filter(user=user)
            for p in participants:
                return c
        return None

    def get_courses(self):
        courses = Course.objects.filter(coursecohort__cohort=self).order_by('title')
        return courses

    def get_leaderboard(self, count=0):
        users = User.objects.filter(participant__cohort=self,
                                    participant__role=Participant.STUDENT,
                                    points__course__coursecohort__cohort=self) \
                            .annotate(total=Sum('points__points')) \
                            .order_by('-total')

        if count != 0:
            users = users[:count]

        for u in users:
            u.badges = Award.objects.filter(user=u, awardcourse__course__coursecohort__cohort=self).count()
            if u.total is None:
                u.total = 0
        return users


class CourseCohort(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    cohort = models.ForeignKey(Cohort, on_delete=models.CASCADE)

    class Meta:
        unique_together = ("course", "cohort")

    
class Participant(models.Model):
    TEACHER = 'teacher'
    STUDENT = 'student'
    ROLE_TYPES = (
        (TEACHER, 'Teacher'),
        (STUDENT, 'Student'),
    )
    cohort = models.ForeignKey(Cohort, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    role = models.CharField(max_length=20, choices=ROLE_TYPES)

    class Meta:
        verbose_name = _('Participant')
        verbose_name_plural = _('Participants')


class Badge(models.Model):
    ref = models.CharField(max_length=20)
    name = models.TextField(blank=False)
    description = models.TextField(blank=True)
    default_icon = models.FileField(upload_to="badges")
    points = models.IntegerField(default=100)
    allow_multiple_awards = models.BooleanField(default=False)

    class Meta:
        verbose_name = _('Badge')
        verbose_name_plural = _('Badges')

    def __unicode__(self):
        return self.description


class Award(models.Model):
    badge = models.ForeignKey(Badge, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    description = models.TextField(blank=False)
    award_date = models.DateTimeField('date awarded', default=timezone.now)

    class Meta:
        verbose_name = _('Award')
        verbose_name_plural = _('Awards')

    def __unicode__(self):
        return self.description

    @staticmethod
    def get_userawards(user, course=None):
        awards = Award.objects.filter(user=user)
        if course is not None:
            awards = awards.filter(awardcourse__course=course)
        return awards.count()

    def _get_badge(self):
        badge_icon = self.badge.default_icon
        try:
            icon = AwardCourse.objects.get(award=self)
            if icon.course.badge_icon:
                return icon.course.badge_icon
        except AwardCourse.DoesNotExist:
            pass
        return badge_icon

    badge_icon = property(_get_badge)


class AwardCourse(models.Model):
    award = models.ForeignKey(Award, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    course_version = models.BigIntegerField(default=0)


class Points(models.Model):
    POINT_TYPES = (
        ('signup', 'Sign up'),
        ('userquizattempt', 'Quiz attempt by user'),
        ('firstattempt', 'First quiz attempt'),
        ('firstattemptscore', 'First attempt score'),
        ('firstattemptbonus', 'Bonus for first attempt score'),
        ('quizattempt', 'Quiz attempt'),
        ('quizcreated', 'Created quiz'),
        ('activitycompleted', 'Activity completed'),
        ('mediaplayed', 'Media played'),
        ('badgeawarded', 'Badge awarded'),
        ('coursedownloaded', 'Course downloaded'),
    )
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, null=True, default=None, on_delete=models.SET_NULL)
    points = models.IntegerField()
    date = models.DateTimeField('date created', default=timezone.now)
    description = models.TextField(blank=False)
    data = models.TextField(blank=True)
    type = models.CharField(max_length=20, choices=POINT_TYPES)

    class Meta:
        verbose_name = _('Points')
        verbose_name_plural = _('Points')

    def __unicode__(self):
        return self.description

    @staticmethod
    def get_leaderboard(count=0, course=None):

        from oppia.summary.models import UserCourseSummary, UserPointsSummary

        if course is not None:
            users = UserCourseSummary.objects.filter(course=course)
            users_points = users.values('user').annotate(points=Sum('points'), badges=Sum('badges_achieved')).order_by('-points')
        else:
            users_points = UserPointsSummary.objects.all().values('user', 'points', 'badges').order_by('-points')

        if count > 0:
            users_points = users_points[:count]

        leaderboard = []
        for u in users_points:
            user = User.objects.get(pk=u['user'])
            user.badges = 0 if u['badges'] is None else u['badges']
            user.total = 0 if u['points'] is None else u['points']
            leaderboard.append(user)

        return leaderboard
    
    @staticmethod
    def get_userscore(user):
        score = Points.objects.filter(user=user).aggregate(total=Sum('points'))
        if score['total'] is None:
            return 0
        return score['total']

    @staticmethod
    def media_points(user, start_date=None, end_date=None, course=None):
        results = Points.objects.filter(user=user, type='mediaplayed')
        if start_date:
            results = results.filter(date__gte=start_date)
        if end_date:
            results = results.filter(date__lte=end_date)
        if course:
            results = results.filter(course=course)
        score = results.aggregate(total=Sum('points'))
        if score['total'] is None:
            return 0
        return score['total']

    @staticmethod
    def page_points(user, start_date=None, end_date=None, course=None):
        results = Points.objects.filter(user=user, type='activitycompleted')
        if start_date:
            results = results.filter(date__gte=start_date)
        if end_date:
            results = results.filter(date__lte=end_date)
        if course:
            results = results.filter(course=course)
        score = results.aggregate(total=Sum('points'))
        if score['total'] is None:
            return 0
        return score['total']

    @staticmethod
    def quiz_points(user, start_date=None, end_date=None, course=None):
        results = Points.objects.filter(user=user).filter(Q(type='firstattempt') | Q(type='firstattemptscore') | Q(type='firstattemptbonus') | Q(type='quizattempt'))
        if start_date:
            results = results.filter(date__gte=start_date)
        if end_date:
            results = results.filter(date__lte=end_date)
        if course:
            results = results.filter(course=course)
        score = results.aggregate(total=Sum('points'))
        if score['total'] is None:
            return 0
        return score['total']
