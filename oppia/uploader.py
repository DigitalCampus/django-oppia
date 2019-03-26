# oppia/uploader.py

import codecs
import json
import os
import shutil
import xml.dom.minidom
from xml.sax.saxutils import unescape
from zipfile import ZipFile, BadZipfile

from django.conf import settings
from django.contrib import messages
from django.utils import timezone
from django.utils.translation import ugettext as _

from gamification.models import CourseGamificationEvent, ActivityGamificationEvent, MediaGamificationEvent, \
    QuizGamificationEvent
from oppia.models import Course, Section, Activity, Media
from quiz.models import Quiz, Question, QuizQuestion, Response, ResponseProps, QuestionProps, QuizProps


def handle_uploaded_file(f, extract_path, request, user):
    zipfilepath = os.path.join(settings.COURSE_UPLOAD_DIR, f.name)

    with open(zipfilepath, 'wb+') as destination:
        for chunk in f.chunks():
            destination.write(chunk)

    try:
        zip_file = ZipFile(zipfilepath)
        zip_file.extractall(path=extract_path)
    except BadZipfile:
        messages.error(request, _("Invalid zip file"), extra_tags="danger")
        return False, 500

    mod_name = ''
    for dir in os.listdir(extract_path)[:1]:
        mod_name = dir

    # check there is at least a sub dir
    if mod_name == '':
        messages.info(request, _("Invalid course zip file"), extra_tags="danger")
        return False, 400

    response = 200
    try:
        course, response = process_course(extract_path, f, mod_name, request, user)
    except Exception as e:
        messages.error(request, e.message, extra_tags="danger")
        return False, 500
    finally:
        # remove the temp upload files
        shutil.rmtree(extract_path, ignore_errors=True)

    return course, response


def process_course(extract_path, f, mod_name, request, user):
    xml_path = os.path.join(extract_path, mod_name, "module.xml")
    # check that the module.xml file exists
    if not os.path.isfile(xml_path):
        messages.info(request, _("Zip file does not contain a module.xml file"), extra_tags="danger")
        return False, 400

    # parse the module.xml file
    doc = xml.dom.minidom.parse(xml_path)
    meta_info = parse_course_meta(doc)

    new_course = False
    oldsections = []
    old_course_filename = None

    # Find if course already exists
    try:
        course = Course.objects.get(shortname=meta_info['shortname'])
        # check that the current user is allowed to wipe out the other course
        if course.user != user:
            messages.info(request, _("Sorry, only the original owner may update this course"))
            return False, 401
        # check if course version is older
        if course.version > meta_info['versionid']:
            messages.info(request, _("A newer version of this course already exists"))
            return False, 400

        # obtain the old sections
        oldsections = list(Section.objects.filter(course=course).values_list('pk', flat=True))
        # wipe out old media
        oldmedia = Media.objects.filter(course=course)
        oldmedia.delete()

        old_course_filename = course.filename
        course.lastupdated_date = timezone.now()

    except Course.DoesNotExist:
        course = Course()
        course.is_draft = True
        new_course = True

    course.shortname = meta_info['shortname']
    course.title = meta_info['title']
    course.description = meta_info['description']
    course.version = meta_info['versionid']
    course.user = user
    course.filename = f.name
    course.save()

    # save gamification events
    if 'gamification' in meta_info:
        events = parse_gamification_events(meta_info['gamification'])
        # remove anything existing for this course
        CourseGamificationEvent.objects.filter(course=course).delete()
        # add new
        for event in events:
            e = CourseGamificationEvent(user=user, course=course, event=event['name'], points=event['points'])
            e.save()

    process_quizzes_locally = False
    if 'exportversion' in meta_info and meta_info['exportversion'] >= settings.OPPIA_EXPORT_LOCAL_MINVERSION:
        process_quizzes_locally = True

    parse_course_contents(request, doc, course, user, new_course, process_quizzes_locally)
    clean_old_course(request, oldsections, old_course_filename, course)

    tmp_path = replace_zip_contents(xml_path, doc, mod_name, extract_path)
    # Extract the final file into the courses area for preview
    zipfilepath = os.path.join(settings.COURSE_UPLOAD_DIR, f.name)
    shutil.copy(tmp_path + ".zip", zipfilepath)

    course_preview_path = settings.MEDIA_ROOT + "courses/"
    ZipFile(zipfilepath).extractall(path=course_preview_path)

    return course, 200


def parse_course_contents(req, xml_doc, course, user, new_course, process_quizzes_locally):
    # add in any baseline activities
    for meta in xml_doc.getElementsByTagName("meta")[:1]:
        if meta.getElementsByTagName("activity").length > 0:
            section = Section(
                course=course,
                title='{"en": "Baseline"}',
                order=0
            )
            section.save()
            for act in meta.getElementsByTagName("activity"):
                parse_and_save_activity(req, user, section, act, new_course, process_quizzes_locally, is_baseline=True)

    # add all the sections and activities
    for structure in xml_doc.getElementsByTagName("structure")[:1]:

        if structure.getElementsByTagName("section").length == 0:
            course.delete()
            messages.info(req, _("There don't appear to be any activities in this upload file."))
            return

        for idx, s in enumerate(structure.getElementsByTagName("section")):

            # Check if the section contains any activity (to avoid saving an empty one)
            activities = s.getElementsByTagName("activities")[:1]
            if not activities or activities[0].getElementsByTagName("activity").length == 0:
                messages.info(req, _("Section ") + str(idx + 1) + _(" does not contain any activities."))
                continue

            title = {}
            for t in s.childNodes:
                if t.nodeName == 'title':
                    title[t.getAttribute('lang')] = t.firstChild.nodeValue
            section = Section(
                course=course,
                title=json.dumps(title),
                order=s.getAttribute("order")
            )
            section.save()

            for activities in s.getElementsByTagName("activities")[:1]:
                for act in activities.getElementsByTagName("activity"):
                    parse_and_save_activity(req, user, section, act, new_course, process_quizzes_locally)

    media_element_list = [node for node in xml_doc.firstChild.childNodes if node.nodeName == 'media']
    media_element = None
    if len(media_element_list) > 0:
        media_element = media_element_list[0]

    if media_element is not None:
        for file_element in media_element.childNodes:
            if file_element.nodeName == 'file':
                media = Media()
                media.course = course
                media.filename = file_element.getAttribute("filename")
                url = file_element.getAttribute("download_url")
                media.digest = file_element.getAttribute("digest")

                if len(url) > Media.URL_MAX_LENGTH:
                    messages.info(req, _('File %(filename)s has a download URL larger than the maximum length permitted. The media file has not been registered, so it won\'t be tracked. Please, fix this issue and upload the course again.') % {'filename': media.filename})
                else:
                    media.download_url = url
                    # get any optional attributes
                    for attr_name, attr_value in file_element.attributes.items():
                        if attr_name == "length":
                            media.media_length = attr_value
                        if attr_name == "filesize":
                            media.filesize = attr_value

                    media.save()
                    # save gamification events
                    if file_element.getElementsByTagName('gamification')[:1]:
                        events = parse_gamification_events(file_element.getElementsByTagName('gamification')[0])
                        # remove anything existing for this course
                        MediaGamificationEvent.objects.filter(media=media).delete()
                        # add new
                        for event in events:
                            e = MediaGamificationEvent(user=user, media=media, event=event['name'], points=event['points'])
                            e.save()


def parse_and_save_activity(req, user, section, act, new_course, process_quiz_locally, is_baseline=False):
    """
    Parses an Activity XML and saves it to the DB
    :param section: section the activity belongs to
    :param act: a XML DOM element containing a single activity
    :param new_course: boolean indicating if it is a new course or existed previously
    :param process_quiz_locally: should the quiz be created based on the JSON contents?
    :param is_baseline: is the activity part of the baseline?
    :return: None
    """
    temp_title = {}
    for t in act.getElementsByTagName("title"):
        temp_title[t.getAttribute('lang')] = t.firstChild.nodeValue
    title = json.dumps(temp_title)

    content = ""
    act_type = act.getAttribute("type")
    if act_type == "page" or act_type == "url":
        temp_content = {}
        for t in act.getElementsByTagName("location"):
            if t.firstChild and t.getAttribute('lang'):
                temp_content[t.getAttribute('lang')] = t.firstChild.nodeValue
        content = json.dumps(temp_content)
    elif act_type == "quiz" or act_type == "feedback":
        for c in act.getElementsByTagName("content"):
            content = c.firstChild.nodeValue
    elif act_type == "resource":
        for c in act.getElementsByTagName("location"):
            content = c.firstChild.nodeValue
    else:
        content = None

    image = None
    if act.getElementsByTagName("image"):
        for i in act.getElementsByTagName("image"):
            image = i.getAttribute('filename')

    if act.getElementsByTagName("description"):
        description = {}
        for d in act.getElementsByTagName("description"):
            if d.firstChild and d.getAttribute('lang'):
                description[d.getAttribute('lang')] = d.firstChild.nodeValue
        description = json.dumps(description)
    else:
        description = None

    digest = act.getAttribute("digest")
    existed = False
    try:
        activity = Activity.objects.get(digest=digest)
        existed = True
    except Activity.DoesNotExist:
        activity = Activity()

    activity.section = section
    activity.title = title
    activity.type = act_type
    activity.order = act.getAttribute("order")
    activity.digest = act.getAttribute("digest")
    activity.baseline = is_baseline
    activity.image = image
    activity.content = content
    activity.description = description

    if not existed and not new_course:
        messages.warning(req, _('Activity "%(act)s"(%(digest)s) did not exist previously.') % {'act': activity, 'digest': activity.digest})
    '''
    If we also want to show the activities that previously existed, uncomment this block
    else:
        messages.info(req, _('Activity "%(act)s"(%(digest)s) previously existed. Updated with new information') % {'act': activity, 'digest':activity.digest})
    '''

    if (act_type == "quiz") and process_quiz_locally:
        updated_json = parse_and_save_quiz(req, user, activity, act)
        # we need to update the JSON contents both in the XML and in the activity data
        act.getElementsByTagName("content")[0].firstChild.nodeValue = updated_json
        activity.content = updated_json

    activity.save()

    # save gamification events
    if act.getElementsByTagName('gamification')[:1]:
        events = parse_gamification_events(act.getElementsByTagName('gamification')[0])
        # remove anything existing for this course
        ActivityGamificationEvent.objects.filter(activity=activity).delete()
        # add new
        for event in events:
            e = ActivityGamificationEvent(user=user, activity=activity, event=event['name'], points=event['points'])
            e.save()


def parse_and_save_quiz(req, user, activity, act_xml):
    """
    Parses an Activity XML that is a Quiz and saves it to the DB
    :parm user: the user that uploaded the course
    :param activity: a XML DOM element containing the activity
    :return: None
    """

    quiz_obj = json.loads(activity.content)

    quiz_existed = False
    # first of all, we find the quiz digest to see if it is already saved
    if quiz_obj['props']['digest']:
        quiz_digest = quiz_obj['props']['digest']

        try:
            quizzes = Quiz.objects.filter(quizprops__value=quiz_digest, quizprops__name="digest").order_by('-id')
            quiz_existed = len(quizzes) > 0
            # remove any possible duplicate (possible scenario when transitioning between export versions)
            for quiz in quizzes[1:]:
                quiz.delete()

        except Quiz.DoesNotExist:
            quiz_existed = False

    if quiz_existed:
        try:
            quiz_act = Activity.objects.get(digest=quiz_digest)
            updated_content = quiz_act.content
        except Activity.DoesNotExist:
            updated_content = create_quiz(user, quiz_obj, act_xml)
    else:
        updated_content = create_quiz(user, quiz_obj, act_xml)

    return updated_content


def create_quiz(user, quiz_obj, act_xml):

    quiz = Quiz()
    quiz.owner = user
    quiz.title = quiz_obj['title']
    quiz.description = quiz_obj['description']
    quiz.save()

    # save gamification events
    if act_xml.getElementsByTagName('gamification')[:1]:
        events = parse_gamification_events(act_xml.getElementsByTagName('gamification')[0])
        # remove anything existing for this course
        QuizGamificationEvent.objects.filter(quiz=quiz).delete()
        # add new
        for event in events:
            e = QuizGamificationEvent(user=user, quiz=quiz, event=event['name'], points=event['points'])
            e.save()

    quiz_obj['id'] = quiz.pk

    # add quiz props
    create_quiz_props(quiz, quiz_obj)

    # add quiz questions
    create_quiz_questions(user, quiz, quiz_obj)

    return json.dumps(quiz_obj)


def parse_course_meta(xml_doc):

    meta_info = {'versionid': 0, 'shortname': ''}
    for meta in xml_doc.getElementsByTagName("meta")[:1]:
        for v in meta.getElementsByTagName("versionid")[:1]:
            meta_info['versionid'] = int(v.firstChild.nodeValue)

        temp_title = {}
        for t in meta.childNodes:
            if t.nodeName == "title":
                temp_title[t.getAttribute('lang')] = t.firstChild.nodeValue
        meta_info['title'] = json.dumps(temp_title)

        temp_description = {}
        for t in meta.childNodes:
            if t.nodeName == "description":
                if t.firstChild is not None:
                    temp_description[t.getAttribute('lang')] = t.firstChild.nodeValue
                else:
                    temp_description[t.getAttribute('lang')] = None
        meta_info['description'] = json.dumps(temp_description)

        for sn in meta.getElementsByTagName("shortname")[:1]:
            meta_info['shortname'] = sn.firstChild.nodeValue

        for v in meta.getElementsByTagName("exportversion")[:1]:
            meta_info['exportversion'] = int(v.firstChild.nodeValue)

        for g in meta.getElementsByTagName("gamification"):
            meta_info['gamification'] = g

    return meta_info


def parse_gamification_events(element):
    events = []
    for e in element.getElementsByTagName("event"):
        event_name = e.getAttribute('name')
        points = e.firstChild.nodeValue
        events.append({'name': event_name, 'points': points})
    return events


def replace_zip_contents(xml_path, xml_doc, mod_name, dest):
    fh = codecs.open(xml_path, mode="w", encoding="utf-8")
    new_xml = xml_doc.toxml("utf-8").decode('utf-8')
    new_xml = unescape(new_xml, {"&apos;": "'", "&quot;": '"', "&nbsp;": " "})
    new_xml = new_xml.replace('&nbsp;', ' ').replace('&amp;', '&').replace('&quot;', '"')

    fh.write(new_xml)
    fh.close()

    tmp_zipfilepath = os.path.join(dest, 'tmp_course')
    shutil.make_archive(tmp_zipfilepath, 'zip', dest, base_dir=mod_name)
    return tmp_zipfilepath


def clean_old_course(req, oldsections, old_course_filename, course):
    for section in oldsections:
        sec = Section.objects.get(pk=section)
        for act in sec.activities():
            messages.info(req, _('Activity "%(act)s"(%(digest)s) is no longer in the course.') % {'act': act, 'digest': act.digest})
        sec.delete()

    if old_course_filename is not None and old_course_filename != course.filename:
        try:
            os.remove( os.path.join(settings.COURSE_UPLOAD_DIR, old_course_filename) )
        except OSError:
            pass
        
# helper functions

def create_quiz_props(quiz, quiz_obj):
    for prop in quiz_obj['props']:
        if prop is not 'id':
            QuizProps(
                quiz=quiz, name=prop,
                value=quiz_obj['props'][prop]
            ).save()

def create_quiz_questions(user, quiz, quiz_obj ):
    for q in quiz_obj['questions']:

        question = Question(owner=user,
                type=q['question']['type'],
                title=q['question']['title'])
        question.save()

        quiz_question = QuizQuestion(quiz=quiz, question=question, order=q['order'])
        quiz_question.save()

        q['id'] = quiz_question.pk
        q['question']['id'] = question.pk

        for prop in q['question']['props']:
            if prop is not 'id':
                QuestionProps(
                    question=question, name=prop,
                    value=q['question']['props'][prop]
                ).save()

        for r in q['question']['responses']:
            response = Response(
                owner=user,
                question=question,
                title=r['title'],
                score=r['score'],
                order=r['order']
            )
            response.save()
            r['id'] = response.pk

            for prop in r['props']:
                if prop is not 'id':
                    ResponseProps(
                        response=response, name=prop,
                        value=r['props'][prop]
                    ).save()
