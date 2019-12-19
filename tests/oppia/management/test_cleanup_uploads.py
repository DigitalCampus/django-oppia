import pytest

from io import StringIO
from django.core.management import call_command
from oppia.test import OppiaTestCase


class CleanUpUploadsTest(OppiaTestCase):

    @pytest.mark.xfail(reason="works on local, but not on Github workflow")
    def test_cleanup_uploads(self):
        out = StringIO()
        call_command('cleanup_uploads', stdout=out)