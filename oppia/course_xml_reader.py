# oppia/course_xml_reader.py
import json
import os
import xml.dom.minidom


class CourseXML():

    def __init__(self, course_xml_path):
        self.doc = xml.dom.minidom.parse(course_xml_path)
        self.sections = []

        for structure in self.doc.getElementsByTagName("structure")[:1]:
            for s in structure.getElementsByTagName("section"):
                temp_title = {}
                for t in s.childNodes:
                    if t.nodeName == 'title':
                        temp_title[t.getAttribute('lang')] = t.firstChild.nodeValue
                title = json.dumps(temp_title)
                section = Section(title)
    
                for activities in s.getElementsByTagName("activities")[:1]:
                    for a in activities.getElementsByTagName("activity"):
                        temp_title = {}
                        for t in a.getElementsByTagName("title"):
                            temp_title[t.getAttribute('lang')] = t.firstChild.nodeValue
                        title = json.dumps(temp_title)
    
                        temp_loc = {}
                        for t in a.getElementsByTagName("location"):
                            temp_loc[t.getAttribute('lang')] = t.firstChild.nodeValue
                        location = json.dumps(temp_loc)
    
                        type = a.getAttribute('type')
                        activity = Activity(title, location, type)
                        section.activities.append(activity)

                self.sections.append(section)


class Section():

    def __init__(self, title):
        self.title = title
        self.activities = []


class Activity():

    def __init__(self, title, location, type):
        self.title = title
        self.location = location
        self.type = type
