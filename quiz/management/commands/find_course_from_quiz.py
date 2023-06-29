import json
from json import JSONDecodeError

from django.core.management import BaseCommand

from oppia.models import Activity, Tracker, Course
from quiz.models import QuizProps
from django.utils.translation import gettext_lazy as _


class Command(BaseCommand):
    help = _(u"Find the associated course and activity for a specific quiz_id")

    def add_arguments(self, parser):
        parser.add_argument('quiz_id', type=int, help='ID of the Quiz you want to find related Course and Activity')

    def handle(self, *args, **options):
        quiz_id = options['quiz_id']
        find_related_course_and_activity_for_quiz(quiz_id)


def find_related_course_and_activity_for_quiz(quiz_id):
    course = None

    try:
        quiz_props_digest = QuizProps.objects.get(quiz_id=quiz_id, name="digest").value
        activities = Activity.objects.filter(digest=quiz_props_digest)
        quiz_activity = None

        if len(activities) == 1:
            quiz_activity = activities[0]
            course = quiz_activity.section.course
        else:
            for activity in activities:
                try:
                    content = json.loads(activity.content)
                    props = content.get("props")
                    if props:
                        course_version = props.get("courseversion")
                        quiz_props_course_version = QuizProps.objects.get(quiz_id=quiz_id, name="courseversion").value
                        if course_version == quiz_props_course_version:
                            course = activity.section.course
                            quiz_activity = activity
                            break
                except JSONDecodeError:
                    pass

        if not course:
            trackers = Tracker.objects.filter(digest=quiz_props_digest).order_by('-tracker_date')
            for tracker in trackers:
                courses = Course.objects.filter(id=tracker.course_id)
                if len(courses) == 1:
                    course = courses[0]
                    break

        if course:
            print(f"Found related course for Quiz with ID={quiz_id}")
            print(f"Course ID: {course.id}")
            if quiz_activity:
                print(f"Activity ID: {quiz_activity.id}")
            else:
                print(f"Related Activity not found")
        else:
            print(f"Unable to find related course for Quiz with ID={quiz_id}")
    except Exception:
        print(f"Unable to find related course for Quiz with ID={quiz_id}")
