import json
from django.db import migrations


def populate_time_taken(apps, schema_editor):
    quizattempt_model = apps.get_model("quiz", "QuizAttempt")
    tracker_model = apps.get_model("oppia", "Tracker")

    print("\nUpdating quiz attempts for time taken."
          "\nThis might take a while, please be patient...")

    trackers = tracker_model.objects.exclude(time_taken=0) \
        .filter(type='quiz')

    counter = 1
    for t in trackers:
        try:
            json_data = json.loads(t.data)
            if 'instance_id' in json_data:
                quizattempt_model.objects \
                    .filter(instance_id=json_data['instance_id']) \
                    .update(time_taken=t.time_taken)

            print("{0}/{1} : {2} updated".format(counter,
                                                 trackers.count(),
                                                 json_data['instance_id']))

            counter += 1
        except json.decoder.JSONDecodeError:
            # ignore
            pass


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
