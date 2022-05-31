from oppia.test import OppiaTestCase


class CronWarningTest(OppiaTestCase):

    fixtures = ['tests/test_user.json',
                'tests/test_oppia.json',
                'tests/test_quiz.json',
                'tests/test_permissions.json',
                'tests/test_coursedailystats.json',
                'default_badges.json',
                'tests/test_course_permissions.json']

    # check will show oppiacron

    # check doesn't show oppiacron

    # check will show summarycron

    # check doesn't show summarycron
