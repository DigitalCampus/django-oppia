# coding: utf-8

"""
Management command to remove any duplicate quiz attempts (based on instance_id)
"""
import os
import time
import django.db.models
import oppia.management.commands

from optparse import make_option

from django.conf import settings
from django.contrib.auth.models import User
from django.core.management import call_command
from django.core.management.base import BaseCommand, CommandError
from django.db.models import Count, Max
from django.utils.translation import ugettext_lazy as _

from oppia.quiz.models import QuizAttempt

class Command(BaseCommand):
    help = _(u"Removes any duplicate quiz attempts based on instance_id")

    def add_arguments(self, parser):
        pass

    def handle(self, *args, **options):
        """
        Remove quizattempts with no UUID
        """
        result = QuizAttempt.objects.filter(instance_id=None).delete()
        print(_(u"\n\n%d quiz attempts removed that had no instance_id\n" % result[0]))

        """
        Remove proper duplicate quizattempts - using max id
        """
        quiz_attempts = QuizAttempt.objects.all().values('instance_id').annotate(dcount=Count('instance_id')).filter(dcount__gte=2)

        for index, quiz_attempt in enumerate(quiz_attempts):
            print("%d/%d" % (index, quiz_attempts.count()))
            exclude = QuizAttempt.objects.filter(instance_id=quiz_attempt['instance_id']).aggregate(max_id=Max('id'))
            deleted = QuizAttempt.objects.filter(instance_id=quiz_attempt['instance_id']).exclude(id=exclude['max_id']).delete()
            print(_(u"%d duplicate quiz attempt(s) removed for instance_id %s based on max id" % (deleted[0], quiz_attempt['instance_id'])))
            
        """
        Remember to run summary cron from start
        """
        if result[0] + quiz_attempts.count() > 0:
            print(_(u"Since duplicates have been found and removed, you should now run `update_summaries` to ensure the dashboard graphs are accurate."))
            accept = raw_input(_(u"Would you like to run `update_summaries` now? [Yes/No]"))
            if accept == 'y':
                call_command('update_summaries', fromstart=True)
