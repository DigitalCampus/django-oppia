import ast
from django.db import migrations

from oppia.uploader import clean_lang_dict


def populate_time_taken(apps, schema_editor):
    quizattempt_model = apps.get_model("quiz", "QuizAttempt")
    tracker_model = apps.get_model("oppia", "Tracker")

    quiz_attempts = quizattempt_model.objects.all() \
        .exclude(instance_id='') \
        .exclude(instance_id=None)
    print("\nUpdating quiz attempts for time taken."
          "\nThis might take a while, please be patient...")
    counter = 1
    for qa in quiz_attempts:
        try:
            tracker = tracker_model.objects.exclude(time_taken=0).get(
                type='quiz',
                data__icontains=qa.instance_id)
            qa.time_taken = tracker.time_taken
            qa.save()
            print("{0}/{1} : {2} updated".format(counter,
                                                 quiz_attempts.count(),
                                                 qa.instance_id))
        except tracker_model.DoesNotExist:
            # pass/ignore
            print("{0}/{1} : {2} not found in tracker table"
                  .format(counter,
                          quiz_attempts.count(),
                          qa.instance_id))
        except tracker_model.MultipleObjectsReturned:
            # pass/ignore
            print("{0}/{1} : {2} too many objects returned"
                  .format(counter,
                          quiz_attempts.count(),
                          qa.instance_id))

        counter += 1

def noop(app, schema_editor):
    # this migration is not reversible
    pass


class Migration(migrations.Migration):

    dependencies = [
        ('quiz', '0014_quizattempt_time_taken'),
    ]

    operations = [
        migrations.RunPython(populate_time_taken, noop),
    ]
