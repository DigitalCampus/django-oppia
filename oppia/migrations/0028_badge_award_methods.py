# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations
from django.utils.translation import ugettext_lazy as _

from settings import constants


def add_badge_methods(apps, schema_editor):

    badge_method = apps.get_model("oppia", "BadgeMethod")

    method = badge_method()
    method.key = "all_activities"
    method.description = _(u"All activities must be completed, including all \
        quizzes passed and all media viewed")
    method.save()
    
    method = badge_method()
    method.key = "final_quiz"
    method.description = _(u"Only the final quiz needs to be completed and \
        passed")
    method.save()
    
    method = badge_method()
    method.key = "all_quizzes"
    method.description = _(u"All quizzes need to be completed and passed")
    method.save()
    
    method = badge_method()
    method.key = "all_quizzes_plus_percent"
    method.description = _(u"All quizzes need to be completed and passed, and \
        a percentage of all other activities completed. This percentage is \
        configurable in the settings")
    method.save()

    badge = apps.get_model("oppia", "Badge")

    try:
        badge_obj = badge.objects.get(ref='coursecompleted')
        badge_obj.default_method = badge_method.objects.get(
            key=settings.BADGE_AWARDING_METHOD)
        badge_obj.save()
    except badge.DoesNotExist:
        complete_badge = badge()
        complete_badge.ref = 'coursecompleted'
        complete_badge.points = 500
        complete_badge.default_method = badge_method.objects.get(
            key=settings.BADGE_AWARDING_METHOD)
        complete_badge.save()

class Migration(migrations.Migration):

    dependencies = [
        ('oppia', '0027_auto_20201206_1845'),
    ]

    operations = [
        migrations.RunPython(add_badge_methods),
    ]