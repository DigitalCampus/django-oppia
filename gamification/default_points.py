
from django.utils.translation import ugettext_lazy as _

OPPIA_GLOBAL_DEFAULT_POINTS = [
        {'event': 'register', 
         'points': 100 }  # given when user first registers
    ]

OPPIA_COURSE_DEFAULT_POINTS = [
        {'event': 'course_downloaded', 
         'points': 50 }  # for downloading a course
    ]

OPPIA_QUIZ_DEFAULT_POINTS = [
        {'event': 'quiz_first_attempt', 
         'points': 20 },  # for the first attempt at a quiz
        {'event': 'quiz_attempt', 
         'points': 10 },  # for any subsequent attempts at a quiz
        {'event': 'quiz_first_attempt_threshold', 
         'points': 100 },  # Threshold for getting bonus points for first attempt at quiz (must be 0-100)
        {'event': 'quiz_first_attempt_bonus', 
         'points': 50 }  # Bonus points for getting over the threshold on first attempt at quiz
    ]

OPPIA_ACTIVITY_DEFAULT_POINTS = [
        {'event': 'activity_completed', 
         'points': 10 }  # for completing an activity
    ]

OPPIA_MEDIA_DEFAULT_POINTS = [
        {'event': 'media_started', 
         'points': 20 },  # for starting media
        {'event': 'media_playing_interval', 
         'points': 30 },  # interval in seconds for which points are given
        {'event': 'media_playing_points_per_interval', 
         'points': 5 },  # no points per interval media is playing
        {'event': 'media_max_points', 
         'points': 200 }  # the maximum number of points available for any single media play
    ]
    
OPPIA_DEFAULT_POINTS = OPPIA_COURSE_DEFAULT_POINTS \
                         + OPPIA_QUIZ_DEFAULT_POINTS \
                         + OPPIA_ACTIVITY_DEFAULT_POINTS \
                         + OPPIA_MEDIA_DEFAULT_POINTS
                         
GAMIFICATION_EVENT_HELPER = {
        'media_started': {'label': _(u'Media started'), 'helper': _(u'')},
        'media_playing_points_per_interval': {'label': _(u'Media points per interval'), 'helper': _(u'')},
        'media_playing_interval': {'label': _(u'Media playing interval'), 'helper': _(u'')},
        'media_max_points': {'label': _(u'Media max points'), 'helper': _(u'')},
        'activity_completed': {'label': _(u'Activity Completed'), 'helper': _(u'')},
        'quiz_first_attempt_bonus': {'label': _(u'Quiz first attempt bonus'), 'helper': _(u'')},
        'quiz_first_attempt_threshold': {'label': _(u'Quiz first attempt threshold'), 'helper': _(u'')},
        'quiz_attempt': {'label': _(u'Quiz attempt'), 'helper': _(u'')},
        'quiz_first_attempt': {'label': _(u'Quiz first attempt'), 'helper': _(u'')},
        'course_downloaded': {'label': _(u'Course downloaded'), 'helper': _(u'Number of points for downloading the course')},
    }
