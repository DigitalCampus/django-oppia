# oppia/models.py
import json
import datetime

from django.conf import settings
from django.contrib.auth.models import User
from django.db import models
from django.db.models import Max, Sum, Q
from django.utils.translation import ugettext_lazy as _

from tastypie.models import create_api_key

from xml.dom.minidom import *

models.signals.post_save.connect(create_api_key, sender=User)


class Course(models.Model):
    user = models.ForeignKey(User)
    created_date = models.DateTimeField('date created',default=datetime.datetime.now)
    lastupdated_date = models.DateTimeField('date updated',default=datetime.datetime.now)
    version = models.BigIntegerField()
    title = models.TextField(blank=False)
    shortname = models.CharField(max_length=20)
    filename = models.CharField(max_length=200)
    badge_icon = models.FileField(upload_to="badges",blank=True, default=None)
    staff_only = models.BooleanField(default=False)
   
    class Meta:
        verbose_name = _('Course')
        verbose_name_plural = _('Courses')
        
    def __unicode__(self):
        return self.get_title(self)
    
    def getAbsPath(self):
        return settings.COURSE_UPLOAD_DIR + self.filename
    
    def get_title(self,lang='en'):
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
     
    def is_first_download(self,user):
        no_attempts = CourseDownload.objects.filter(user=user,course=self).count()
        is_first_download = False
        if no_attempts == 1:
            is_first_download = True
        return is_first_download
    
    def no_downloads(self):
        no_downloads = CourseDownload.objects.filter(course=self).count()
        return no_downloads
    
    def no_distinct_downloads(self):
        no_distinct_downloads = CourseDownload.objects.filter(course=self).values('user_id').distinct().count()
        return no_distinct_downloads
    
    def get_default_schedule(self):
        try:
            schedule = Schedule.objects.get(default=True,course = self)
        except Schedule.DoesNotExist:
            return None
        return schedule
    
    def get_activity_today(self):
        return Tracker.objects.filter(course=self,
                                      tracker_date__day=datetime.datetime.now().day,
                                      tracker_date__month=datetime.datetime.now().month,
                                      tracker_date__year=datetime.datetime.now().year).count()
       
    def get_activity_week(self):
        now = datetime.datetime.now()
        last_week = datetime.datetime(now.year, now.month, now.day) - datetime.timedelta(days=7)
        return Tracker.objects.filter(course=self,
                                      tracker_date__gte=last_week).count()
                                      
    def has_quizzes(self):
        quiz_count = Activity.objects.filter(section__course=self,type='quiz').count()
        if quiz_count > 0:
            return True
        else:
            return False
    
class Tag(models.Model):
    name = models.TextField(blank=False)
    created_date = models.DateTimeField('date created',default=datetime.datetime.now)
    created_by = models.ForeignKey(User)
    courses = models.ManyToManyField(Course, through='CourseTag')
    
    class Meta:
        verbose_name = _('Tag')
        verbose_name_plural = _('Tags')
        
    def __unicode__(self):
        return self.name
 
class CourseTag(models.Model):
    course = models.ForeignKey(Course)
    tag = models.ForeignKey(Tag)
    
    class Meta:
        verbose_name = _('Course Tag')
        verbose_name_plural = _('Course Tags')
           
class Schedule(models.Model):
    title = models.TextField(blank=False)
    course = models.ForeignKey(Course)
    default = models.BooleanField(default=False)
    created_date = models.DateTimeField('date created',default=datetime.datetime.now)
    lastupdated_date = models.DateTimeField('date updated',default=datetime.datetime.now)
    created_by = models.ForeignKey(User)
    
    class Meta:
        verbose_name = _('Schedule')
        verbose_name_plural = _('Schedules')
        
    def __unicode__(self):
        return self.title
    
    def to_xml_string(self):
        doc = Document();
        schedule = doc.createElement('schedule')
        schedule.setAttribute('version',self.lastupdated_date.strftime('%Y%m%d%H%M%S'))
        doc.appendChild(schedule)
        act_scheds = ActivitySchedule.objects.filter(schedule=self)
        for acts in act_scheds:
            act = doc.createElement('activity')
            act.setAttribute('digest',acts.digest)
            act.setAttribute('startdate',acts.start_date.strftime('%Y-%m-%d %H:%M:%S'))
            act.setAttribute('enddate',acts.end_date.strftime('%Y-%m-%d %H:%M:%S'))
            schedule.appendChild(act)
        return doc.toxml()
        
class ActivitySchedule(models.Model):
    schedule = models.ForeignKey(Schedule)
    digest = models.CharField(max_length=100)
    start_date = models.DateTimeField(default=datetime.datetime.now)
    end_date = models.DateTimeField(default=datetime.datetime.now)
    
    class Meta:
        verbose_name = _('ActivitySchedule')
        verbose_name_plural = _('ActivitySchedules')
           
class Section(models.Model):
    course = models.ForeignKey(Course)
    order = models.IntegerField()
    title = models.TextField(blank=False)
    
    class Meta:
        verbose_name = _('Section')
        verbose_name_plural = _('Sections')
        
    def __unicode__(self):
        return self.get_title()
    
    def get_title(self,lang='en'):
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
    
class Activity(models.Model):
    section = models.ForeignKey(Section)
    order = models.IntegerField()
    title = models.TextField(blank=False)
    type = models.CharField(max_length=10)
    digest = models.CharField(max_length=100)
    baseline = models.BooleanField(default=False)
    
    def __unicode__(self):
        return self.get_title()
    
    class Meta:
        verbose_name = _('Activity')
        verbose_name_plural = _('Activities')
        
    def get_title(self,lang='en'):
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
    
class Media(models.Model):
    course = models.ForeignKey(Course)
    digest = models.CharField(max_length=100)
    filename = models.CharField(max_length=200)
    download_url = models.URLField()
    
    class Meta:
        verbose_name = _('Media')
        verbose_name_plural = _('Media')
        
    def __unicode__(self):
        return self.filename
    
class Tracker(models.Model):
    user = models.ForeignKey(User)
    submitted_date = models.DateTimeField('date submitted',default=datetime.datetime.now)
    tracker_date = models.DateTimeField('date tracked',default=datetime.datetime.now)
    ip = models.IPAddressField()
    agent = models.TextField(blank=True)
    digest = models.CharField(max_length=100)
    data = models.TextField(blank=True)
    course = models.ForeignKey(Course,null=True, blank=True, default=None)
    type = models.CharField(max_length=10,null=True, blank=True, default=None)
    completed = models.BooleanField(default=False)
    time_taken = models.IntegerField(default=0)
    
    class Meta:
        verbose_name = _('Tracker')
        verbose_name_plural = _('Trackers')
        
    def __unicode__(self):
        return self.agent
    
    def is_first_tracker_today(self):
        olddate = datetime.datetime.now() + datetime.timedelta(hours=-24)
        no_attempts_today = Tracker.objects.filter(user=self.user,digest=self.digest,completed=True,submitted_date__gte=olddate).count()
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
        
    def get_activity_title(self):
        activities = Activity.objects.filter(digest=self.digest)
        for a in activities:
            return a.get_title() + " (" + a.section.get_title() +")"
        media = Media.objects.filter(digest=self.digest)
        for m in media:
            return m.filename
        return "Not found"
    
    def activity_exists(self):
        activities = Activity.objects.filter(digest=self.digest).count()
        if activities >= 1:
            return True
        media = Media.objects.filter(digest=self.digest).count()
        if media >= 1:
            return True
        return False
 
    @staticmethod
    def has_completed_trackers(course,user):
        count = Tracker.objects.filter(user=user, course=course,completed=True).count()        
        if count > 0:
            return True
        return False
     
    @staticmethod
    def to_xml_string(course,user):
        doc = Document();
        trackerXML = doc.createElement('trackers')
        doc.appendChild(trackerXML)
        trackers = Tracker.objects.filter(user=user, course=course,completed=True).values('digest').annotate(max_tracker=Max('submitted_date'))
        for t in trackers:
            track = doc.createElement('tracker')
            track.setAttribute('digest',t['digest'])
            track.setAttribute('submitteddate',t['max_tracker'].strftime('%Y-%m-%d %H:%M:%S'))
            trackerXML.appendChild(track)
        return doc.toxml() 
    
    @staticmethod
    def activity_views(user,type,start_date=None,end_date=None,course=None):
        results = Tracker.objects.filter(user=user,type=type)
        if start_date:
            results = results.filter(submitted_date__gte=start_date)
        if end_date:
            results = results.filter(submitted_date__lte=end_date)
        if course:
            results = results.filter(course=course)
        return results.count()
    
    @staticmethod
    def activity_secs(user,type,start_date=None,end_date=None,course=None):
        results = Tracker.objects.filter(user=user,type=type)
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
        
         
class CourseDownload(models.Model):
    user = models.ForeignKey(User)
    course = models.ForeignKey(Course)
    download_date = models.DateTimeField('date downloaded',default=datetime.datetime.now)
    course_version = models.BigIntegerField(default=0)
    ip = models.IPAddressField(blank=True,default=None)
    agent = models.TextField(blank=True,default=None)
    
    class Meta:
        verbose_name = _('CourseDownload')
        verbose_name_plural = _('CourseDownloads')
 
class Cohort(models.Model):
    course = models.ForeignKey(Course)  
    description = models.CharField(max_length=100)
    start_date = models.DateTimeField(default=datetime.datetime.now)
    end_date = models.DateTimeField(default=datetime.datetime.now)
    schedule = models.ForeignKey(Schedule,null=True, blank=True, default=None)
    
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
    def student_member_now(course,user):
        now = datetime.datetime.now()
        cohorts = Cohort.objects.filter(course=course,start_date__lte=now,end_date__gte=now)
        for c in cohorts:
            participants = c.participant_set.filter(user=user,role=Participant.STUDENT)
            for p in participants:
                return c
        return None
    
    @staticmethod
    def teacher_member_now(course,user):
        now = datetime.datetime.now()
        cohorts = Cohort.objects.filter(course=course,start_date__lte=now,end_date__gte=now)
        for c in cohorts:
            participants = c.participant_set.filter(user=user,role=Participant.TEACHER)
            for p in participants:
                return c
        return None
    
    @staticmethod
    def member_now(course,user):
        now = datetime.datetime.now()
        cohorts = Cohort.objects.filter(course=course,start_date__lte=now,end_date__gte=now)
        for c in cohorts:
            participants = c.participant_set.filter(user=user)
            for p in participants:
                return c
        return None
    
class Participant(models.Model):
    TEACHER = 'teacher'
    STUDENT = 'student'
    ROLE_TYPES = (
        (TEACHER, 'Teacher'),
        (STUDENT, 'Student'),
    )
    cohort = models.ForeignKey(Cohort)
    user = models.ForeignKey(User)
    role = models.CharField(max_length=20,choices=ROLE_TYPES)
    
    class Meta:
        verbose_name = _('Participant')
        verbose_name_plural = _('Participants')
         
class Message(models.Model):
    course = models.ForeignKey(Course) 
    author = models.ForeignKey(User)
    date_created = models.DateTimeField(default=datetime.datetime.now)
    publish_date = models.DateTimeField(default=datetime.datetime.now)
    message = models.CharField(max_length=200)
    link = models.URLField(max_length=255)  
    icon = models.CharField(max_length=200)
    
    class Meta:
        verbose_name = _('Message')
        verbose_name_plural = _('Messages')
        
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
    badge = models.ForeignKey(Badge)
    user = models.ForeignKey(User)
    description = models.TextField(blank=False)
    award_date = models.DateTimeField('date awarded',default=datetime.datetime.now)
    
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
    award = models.ForeignKey(Award)
    course = models.ForeignKey(Course)
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
    user = models.ForeignKey(User)
    course = models.ForeignKey(Course,null=True)
    cohort = models.ForeignKey(Cohort,null=True)
    points = models.IntegerField()
    date = models.DateTimeField('date created',default=datetime.datetime.now)
    description = models.TextField(blank=False)
    data = models.TextField(blank=True)
    type = models.CharField(max_length=20,choices=POINT_TYPES)

    class Meta:
        verbose_name = _('Points')
        verbose_name_plural = _('Points')
        
    def __unicode__(self):
        return self.description
    
    @staticmethod
    def get_leaderboard(count=0, course=None, cohort=None):
        users = User.objects.all()
        
        if course is not None:
            users = users.filter(points__course=course)
        
        if cohort is not None:
            users = users.filter(points__cohort=cohort)
               
        if count == 0:
            users = users.annotate(total=Sum('points__points')).order_by('-total')
        else:
            users = users.annotate(total=Sum('points__points')).order_by('-total')[:count]
            
        for u in users:
            u.badges = Award.get_userawards(u,course)
            if u.total is None:
                u.total = 0
        return users
    
    @staticmethod
    def get_userscore(user):
        score = Points.objects.filter(user=user).aggregate(total=Sum('points'))
        if score['total'] is None:
            return 0
        return score['total']
    
    @staticmethod
    def media_points(user,start_date=None,end_date=None,course=None):
        results = Points.objects.filter(user=user,type='mediaplayed')
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
    def page_points(user,start_date=None,end_date=None,course=None):
        results = Points.objects.filter(user=user,type='activitycompleted')
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
    def quiz_points(user,start_date=None,end_date=None,course=None):
        results = Points.objects.filter(user=user).filter(Q(type='firstattempt') | Q(type='firstattemptscore') | Q(type='firstattemptbonus')| Q(type='quizattempt'))
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
    

    
    