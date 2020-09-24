import pytest

from io import StringIO
from django.core.management import call_command
from oppia.test import OppiaTestCase

from oppia.models import Media


class MediaURLCheckTest(OppiaTestCase):

    fixtures = ['tests/test_user.json',
                'tests/test_oppia.json',
                'tests/test_quiz.json',
                'tests/test_permissions.json',
                'default_badges.json',
                'tests/test_course_permissions.json']

    @pytest.mark.xfail(reason="works on local, but not on Github workflow")
    def test_media_url(self):
        out = StringIO()
        call_command('media_url_check', stdout=out)
        self.assertEqual(u'Checking: who-why-did-mrs-x-die-20140220.m4v',
                         out.getvalue()[0:44])

    @pytest.mark.xfail(reason="works on local, but not on Github workflow")
    def test_media_url_invalid_url(self):
        media = Media.objects.get(pk=1)
        original_download_url = media.download_url
        media.download_url = \
            "http://invalid/media/anc/who-why-did-mrs-x-die-20140220.m4v"
        media.save()

        out = StringIO()
        call_command('media_url_check', stdout=out)
        self.assertEqual(u'Checking: who-why-did-mrs-x-die-20140220.m4v',
                         out.getvalue()[0:44])
        contains_warning = False
        if "WARNING: media file not found at" in out.getvalue():
            contains_warning = True
        self.assertEqual(True, contains_warning)

        # reset download url
        media.download_url = original_download_url
        media.save()

    @pytest.mark.xfail(reason="works on local, but not on Github workflow")
    def test_media_url_filesize_mismatch(self):
        media = Media.objects.get(pk=1)
        original_filesize = media.filesize
        media.filesize = 1234
        media.save()

        out = StringIO()
        call_command('media_url_check', stdout=out)
        self.assertEqual(u'Checking: who-why-did-mrs-x-die-20140220.m4v',
                         out.getvalue()[0:44])
        contains_warning = False
        if "INFO: file sizes appear to be different:" in out.getvalue():
            contains_warning = True
        self.assertEqual(True, contains_warning)

        # reset download url
        media.filesize = original_filesize
        media.save()
