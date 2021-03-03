
from django.core.management import call_command

from io import StringIO

from oppia.models import Category
from oppia.test import OppiaTestCase


class CleanCategoriesTest(OppiaTestCase):

    def test_data_retention_no_delete(self):
        out = StringIO()

        start_tag_count = Category.objects.all().count()
        call_command('clean_categories', stdout=out)
        end_tag_count = Category.objects.all().count()
        self.assertEqual(start_tag_count, end_tag_count)

    def test_data_retention_with_delete(self):
        out = StringIO()

        c = Category()
        c.name = "new tag"
        c.save()

        start_c_count = Category.objects.all().count()
        call_command('clean_categories', stdout=out)
        end_c_count = Category.objects.all().count()
        self.assertEqual(start_c_count-1, end_c_count)
