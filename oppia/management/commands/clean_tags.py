
from django.core.management import call_command
from django.core.management.base import BaseCommand
from django.db.models import Exists, OuterRef
from django.utils.translation import ugettext_lazy as _

from oppia.models import CourseTag, Tag


class Command(BaseCommand):
    help = 'OppiaMobile command to remove any unused tags'


    def handle(self, *args, **options):
        unused_tags = Tag.objects.annotate(
            no_courses=~Exists(CourseTag.objects.filter(tag__pk=OuterRef('pk')))
            ).filter(
                no_courses=True
            )
        
        if unused_tags.count() == 0:
            print(_(u"There are no unsed tags to be removed"))
            return
        
        for tag in unused_tags:
            tag.delete()
            print(_(u"%s deleted as unused" % tag))
        