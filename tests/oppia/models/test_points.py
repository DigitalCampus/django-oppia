from oppia.test import OppiaTestCase


class PointsModelTest(OppiaTestCase):
    fixtures = ['tests/test_user.json',
                'tests/test_oppia.json',
                'tests/test_quiz.json',
                'tests/test_permissions.json',
                'default_gamification_events.json',
                'tests/test_tracker.json',
                'tests/test_gamification.json',
                'tests/test_course_permissions.json']
