
from django.core.management.base import BaseCommand
from django.db.models import Exists, OuterRef
from django.utils.translation import gettext_lazy as _

from oppia.models import CourseCategory, Category


class Command(BaseCommand):
    help = 'OppiaMobile command to remove any unused categories'

    def handle(self, *args, **options):
        unused_categories = Category.objects.annotate(
            no_courses=~Exists(CourseCategory.objects.filter(
                category__pk=OuterRef('pk')))).filter(no_courses=True)

        if unused_categories.count() == 0:
            print(_(u"There are no unused categories to be removed"))
            return

        for category in unused_categories:
            category.delete()
            print(_(u"%s deleted as unused" % category))
