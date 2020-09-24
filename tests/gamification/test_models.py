
from oppia.test import OppiaTestCase

from gamification.models import DefaultGamificationEvent, \
                                CourseGamificationEvent, \
                                ActivityGamificationEvent, \
                                MediaGamificationEvent


class GamificationModelsTest(OppiaTestCase):
    fixtures = ['tests/test_user.json',
                'tests/test_oppia.json',
                'tests/test_quiz.json',
                'default_gamification_events.json',
                'tests/test_gamification.json',
                'tests/test_course_permissions.json']

    def test_default_event_str(self):
        event = DefaultGamificationEvent.objects.get(pk=1)
        self.assertEqual("register", str(event))

    def test_course_event_str(self):
        event = CourseGamificationEvent.objects.get(pk=9)
        self.assertEqual("media_max_points", str(event))

    def test_activity_event_str(self):
        event = ActivityGamificationEvent.objects.get(pk=2)
        self.assertEqual("activity_completed", str(event))

    def test_media_event_str(self):
        event = MediaGamificationEvent.objects.get(pk=2)
        self.assertEqual("media_playing_interval", str(event))

    def test_event_default(self):
        event = MediaGamificationEvent.objects.get(pk=2)
        self.assertEqual(9, event.default_event.id)

    def test_event_label(self):
        event = CourseGamificationEvent.objects.get(pk=2)
        self.assertEqual("Quiz attempt", event.get_label())

    def test_event_helper_text(self):
        event = CourseGamificationEvent.objects.get(pk=2)
        self.assertEqual("Number of points for attempting a quiz",
                         event.get_helper_text())
