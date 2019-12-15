import pytest

from io import StringIO
from django.core.management import call_command
from django.test import TestCase


class CleanUpUploadsTest(TestCase):
    fixtures = ['tests/test_user.json',
                'tests/test_oppia.json',
                'tests/test_quiz.json',
                'tests/test_permissions.json']

    def setUp(self):
        super(CleanUpUploadsTest, self).setUp()

    @pytest.mark.xfail(reason="works on local, but not on Github workflow")
    def test_cleanup_uploads(self):
        out = StringIO()
        call_command('cleanup_uploads', stdout=out)