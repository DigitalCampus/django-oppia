import json
import shutil
from zipfile import ZipFile, BadZipfile

import os
import xml.etree.ElementTree as ET
from django.conf import settings
from django.core.management.base import BaseCommand
from django.utils.translation import gettext_lazy as _

from oppia.models import Course, Activity, Section
from oppia.uploader import get_activity_content, parse_and_save_quiz
from quiz.models import Quiz


class Command(BaseCommand):
    help = 'Regenerate course structure, parsing again its XML'

    def add_arguments(self, parser):
        parser.add_argument('shortname',
                            type=str,
                            help='Shortname of the course to parse again')

    def handle(self, *args, **options):

        shortname = options['shortname']
        course = Course.objects.get(shortname=shortname)

        course_count = Activity.objects.filter(section__course=course).count()
        act_count = Activity.objects.all().count()
        quiz_count = Quiz.objects.all().count()
        print("Count: {} course activities, {} total, {} quizzes"
              .format(course_count, act_count, quiz_count))

        extract_path = os.path.join(settings.COURSE_UPLOAD_DIR,
                                    'temp', '0')

        try:
            zip_file = ZipFile(course.getAbsPath())
            zip_file.extractall(path=extract_path)
        except (OSError, BadZipfile):
            msg_text = _(u"Invalid zip file")
            print(msg_text)
            shutil.rmtree(extract_path, ignore_errors=True)
            exit(-1)

        xml_path = os.path.join(extract_path, shortname, "module.xml")
        # parse the module.xml file
        xml_doc = ET.parse(xml_path)

        # obtain the old sections
        oldsections = list(Section.objects.filter(course=course)
                           .values_list('pk', flat=True))

        # add in any baseline activities
        self.parse_baseline_activities(xml_doc, course, False)

        # add all the sections and activities
        structure = xml_doc.find("structure")
        self.process_course_sections(structure, course, False)

        for section in oldsections:
            sec = Section.objects.get(pk=section)
            sec.delete()

        course_count = Activity.objects.filter(section__course=course).count()
        act_count = Activity.objects.all().count()
        quiz_count = Quiz.objects.all().count()
        print("Count: {} course activities, {} total, {} quizzes"
              .format(course_count, act_count, quiz_count))

    def process_course_sections(self, structure, course, is_new_course):
        for index, section in enumerate(structure.findall("section")):

            activities = section.find('activities')
            # Check if the section contains any activity
            # (to avoid saving an empty one)
            if activities is None or len(activities.findall('activity')) == 0:
                continue

            title = {}
            for t in section.findall('title'):
                title[t.get('lang')] = t.text

            section = Section(
                course=course,
                title=json.dumps(title),
                order=section.get('order')
            )
            section.save()

            for act in activities.findall("activity"):
                self.parse_and_save_activity(course, section, act, False)

    def parse_baseline_activities(self, xml_doc, course, is_new_course):

        for meta in xml_doc.findall('meta')[:1]:
            activity_nodes = meta.findall("activity")
            if len(activity_nodes) > 0:
                section = Section(
                    course=course,
                    title='{"en": "Baseline"}',
                    order=0
                )
                section.save()
                for activity_node in activity_nodes:
                    self.parse_and_save_activity(course,
                                                 section,
                                                 activity_node,
                                                 is_new_course,
                                                 True)

    def parse_and_save_activity(self,
                                course,
                                section,
                                activity_node,
                                is_new_course,
                                is_baseline=False):
        """
        Parses an Activity XML and saves it to the DB
        :param section: section the activity belongs to
        :param act: a XML DOM element containing a single activity
        :param is_new_course: boolean indicating if it is a new course or existed
                previously
        :param is_baseline: is the activity part of the baseline?
        :return: None
        """

        title = {}
        for t in activity_node.findall('title'):
            title[t.get('lang')] = t.text
        title = json.dumps(title) if title else None

        description = {}
        for t in activity_node.findall('description'):
            description[t.get('lang')] = t.text
        description = json.dumps(description) if description else None

        content, activity_type = get_activity_content(activity_node)

        image = None
        for i in activity_node.findall("image"):
            image = i.get('filename')

        digest = activity_node.get("digest")
        try:
            activity = Activity.objects.get(
                digest=digest, section__course__shortname=course.shortname)
        except Activity.DoesNotExist:
            activity = Activity()

        activity.section = section
        activity.title = title
        activity.type = activity_type
        activity.order = activity_node.get("order")
        activity.digest = digest
        activity.baseline = is_baseline
        activity.image = image
        activity.content = content
        activity.description = description

        if (activity_type == "quiz") or (activity_type == "feedback"):
            updated_json = parse_and_save_quiz(user=None, activity=activity)
            # we need to update the JSON contents both in the XML and in the
            # activity data
            activity_node.find("content").text = \
                "<![CDATA[ " + updated_json + "]]>"
            activity.content = updated_json

        activity.save()
