import os
import xml
import zipfile

import datetime

from django.utils import timezone
from django.conf import settings

from gamification.models import CourseGamificationEvent
from oppia.models import Activity, Media
from oppia.utils import course_file

GAMIFICATION_NODE = 'gamification'
ACTIVITY_NODE = 'activity'
MEDIA_NODE = 'media'
ACTIVITY_DIGEST_ATTR = 'digest'


class GamificationXMLWriter:

    def __init__(self, course):
        self.course = course
        self.xml = None
        self.xml_contents = None

    def find_child_node_by_name(self, parent, name):
        for node in parent.childNodes:
            if node.nodeType == node.ELEMENT_NODE and node.tagName == name:
                return node
        return None

    def remove_node(self, node):
        parent = node.parentNode
        parent.removeChild(node)

    def load_course_xml_content(self, mode='r'):
        course_zip_file = os.path.join(settings.COURSE_UPLOAD_DIR,
                                       self.course.filename)

        course_zip = zipfile.ZipFile(course_zip_file, mode)
        self.xml_contents = course_zip.read(self.course.shortname + "/module.xml")
        course_zip.close()

        self.xml = xml.dom.minidom.parseString(self.xml_contents)

    def update_course_version(self):
        new_version_id = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
        # update db
        self.course.version = new_version_id
        self.course.lastupdated_date = timezone.now()
        self.course.save()

        meta = self.xml.getElementsByTagName("meta")[:1][0]
        version_id = meta.getElementsByTagName("versionid")[0]
        version_id.firstChild.nodeValue = new_version_id
        return new_version_id

    def get_or_create_gamication_node(self, parent):
        if parent is None:
            return None

        node = self.find_child_node_by_name(parent, GAMIFICATION_NODE)
        if not node:
            # If we didn't find it, create a new node
            node = self.xml.createElement(GAMIFICATION_NODE)
            parent.appendChild(node)
        return node

    def get_or_create_global_node(self):
        meta = self.xml.getElementsByTagName("meta")[:1][0]
        return self.get_or_create_gamication_node(meta)

    def get_or_create_activity_node(self, activity):
        activity_node = None
        for node in self.xml.getElementsByTagName(ACTIVITY_NODE):
            if node.getAttribute(ACTIVITY_DIGEST_ATTR) == activity.digest:
                activity_node = node

        return self.get_or_create_gamication_node(activity_node)

    def get_or_create_media_node(self, media):

        file_node = None
        media_node = self.find_child_node_by_name(self.xml.firstChild,
                                                  MEDIA_NODE)
        for node in media_node.getElementsByTagName('file'):
            if node.getAttribute(ACTIVITY_DIGEST_ATTR) == media.digest:
                file_node = node

        return self.get_or_create_gamication_node(file_node)

    def add_events_or_remove_node(self, node, events):
        if len(events) > 0:

            # Remove previous event nodes
            while node.hasChildNodes():
                node.removeChild(node.firstChild)

            for event in events:
                points = self.xml.createTextNode(str(event.points))
                event_node = self.xml.createElement("event")
                event_node.setAttribute("name", event.event)
                event_node.appendChild(points)
                node.appendChild(event_node)

        else:
            # if there are no events set, we can remove the empty gamification
            # node
            self.remove_node(node)

    def update_course_gamification(self):
        # Update course level gamification
        course_gamif = self.get_or_create_global_node()
        course_events = CourseGamificationEvent.objects \
            .filter(course=self.course)
        self.add_events_or_remove_node(course_gamif, course_events)

    def update_activity_gamification(self):
        # Update activity level gamification
        activities = Activity.objects.filter(section__course=self.course)
        for activity in activities:
            act_gamif = self.get_or_create_activity_node(activity)
            act_events = activity.gamification_events.all()
            self.add_events_or_remove_node(act_gamif, act_events)

    def update_media_gamification(self):
        # Update media level gamification
        course_media = Media.objects.filter(course=self.course)
        for media in course_media:
            media_gamif = self.get_or_create_media_node(media)
            media_events = media.gamification_events.all()
            self.add_events_or_remove_node(media_gamif, media_events)

    def update_gamification(self, user):

        print('parsing course XML')
        self.load_course_xml_content(mode='r')

        print('Updating gamification XML nodes...')
        self.update_course_gamification()
        self.update_activity_gamification()
        self.update_media_gamification()

        version = self.update_course_version()
        print('Writing new course XML contents...')
        course_file.rewrite_xml_contents(user, self.course, self.xml)

        return version
