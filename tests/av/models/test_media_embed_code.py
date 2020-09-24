import pytest
import re

from oppia.test import OppiaTestCase
from av.models import UploadedMedia


class MediaEmbedCodeTest(OppiaTestCase):

    fixtures = ['tests/test_user.json',
                'tests/test_oppia.json',
                'tests/test_permissions.json',
                'tests/test_av_uploadedmedia.json',
                'tests/test_course_permissions.json']

    expected_embed_output = "[[media \
        object='{\"filename\":\"ldrshp-mgmt-unit-2-risk-mgmt-D-v2.m4v\", \
        \"download_url\":\"https://download.digital-campus.org/\", \
        \"digest\":\"33e2c3cfc3e91d06b8a826f626fe39c3\", \
        \"filesize\":0, \
        \"length\":82}']]IMAGE/TEXT HERE[[/media]]"

    @pytest.mark.xfail(reason="works on local, but not on Github workflow")
    def test_media_embed_code(self):
        uploaded_media = UploadedMedia.objects.get(pk=1)
        embed_code = uploaded_media. \
            get_embed_code('https://download.digital-campus.org/')
        supplied_embed_code = re.sub(' +', ' ', embed_code)
        expected_embed_code = re.sub(' +', ' ', self.expected_embed_output)
        self.assertEqual(supplied_embed_code, expected_embed_code)
