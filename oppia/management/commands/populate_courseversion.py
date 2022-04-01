# coding: utf-8

"""
Management command to populate course_version (to run after applying the
"0042_tracker_course_version" migration
"""

from django.core.management.base import BaseCommand
from django.utils.translation import gettext_lazy as _

from oppia.models import Tracker, Activity
from settings.models import SettingProperties

BATCH_PROCESS_SIZE = 500


class Command(BaseCommand):
    help = _(u"Populates the course_version field in the tracker model based \
               on the current course activities")

    def handle(self, *args, **options):
        """
        Populates the course_version field in the tracker model based on the
        current course activities
        """

        newest_tracker_pk = Tracker.objects.latest('id').id
        init_tracker_pk = SettingProperties.get_property(
            'last_courseversion_populated_tracker_pk', 0)

        if newest_tracker_pk <= init_tracker_pk:
            print("No more trackers to process!")
            return

        trackers = Tracker.objects.filter(digest__isnull=False,
                                          pk__gt=init_tracker_pk,
                                          course__isnull=False,
                                          course_version__isnull=True)
        print("{} total trackers to process".format(trackers.count()))

        while newest_tracker_pk > init_tracker_pk:

            end_tracker_pk = min(init_tracker_pk + BATCH_PROCESS_SIZE,
                                 newest_tracker_pk)
            self.process_batch(init_tracker_pk, end_tracker_pk)

            SettingProperties.set_int(
                'last_courseversion_populated_tracker_pk', end_tracker_pk)
            init_tracker_pk = end_tracker_pk

    def process_batch(self, init_tracker_pk, end_tracker_pk):

        trackers = Tracker.objects.filter(digest__isnull=False,
                                          pk__gt=init_tracker_pk,
                                          pk__lte=end_tracker_pk,
                                          course__isnull=False,
                                          course_version__isnull=True)

        print("Processing trackers {} - {}".format(init_tracker_pk,
                                                   end_tracker_pk))

        count = 0
        trackcount = 0
        for tracker in trackers:
            trackcount += 1
            act = Activity.objects.filter(digest=tracker.digest).first()
            if act:
                count += 1
                tracker.course_version = act.section.course.version
                tracker.save()

        print("Added course version to {} out of {} activity trackers"
              .format(count, trackcount))
