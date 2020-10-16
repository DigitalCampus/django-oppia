from django.conf import settings
from django.core.management import call_command

from io import StringIO

from oppia.models import Tag
from oppia.test import OppiaTestCase


class CleanTagsTest(OppiaTestCase):


     def test_data_retention_no_delete(self):
        out = StringIO()

        start_tag_count = Tag.objects.all().count()
        call_command('clean_tags', stdout=out)
        end_tag_count = Tag.objects.all().count()
        self.assertEqual(start_tag_count, end_tag_count)

     def test_data_retention_with_delete(self):
        out = StringIO()

        tag = Tag()
        tag.name = "new tag"
        tag.save()

        start_tag_count = Tag.objects.all().count()
        call_command('clean_tags', stdout=out)
        end_tag_count = Tag.objects.all().count()
        self.assertEqual(start_tag_count-1, end_tag_count)
