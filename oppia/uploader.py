# oppia/uploader.py

import codecs
import json
import logging
import os
import shutil
from zipfile import ZipFile, BadZipfile

import xml.etree.ElementTree as ET

from django.conf import settings
from django.contrib import messages
from django.utils import timezone
from django.utils.translation import gettext as _

from gamification.models import CourseGamificationEvent, \
                                ActivityGamificationEvent, \
                                MediaGamificationEvent
from gamification.xml_writer import GamificationXMLWriter
from oppia.models import Course, \
    Section, \
    Activity, \
    Media, \
    CoursePublishingLog, \
    CoursePermissions, CourseStatus
from oppia.utils.course_file import unescape_xml
from quiz.models import Quiz, \
                        Question, \
                        QuizQuestion, \
                        Response, \
                        ResponseProps, \
                        QuestionProps, \
                        QuizProps

# Get an instance of a logger
logger = logging.getLogger(__name__)


def clean_lang_dict(elem_content):
    if isinstance(elem_content, dict):
        for lang in elem_content:
            elem_content[lang] = elem_content[lang] \
                .strip() \
                .replace(u"\u00A0", " ")
            return json.dumps(elem_content)
    elif isinstance(elem_content, str):
        return elem_content.strip().replace(u"\u00A0", " ")
    else:
        # If it was a boolean or a number (for some response types),
        # return the value as is
        return elem_content


def get_course_shortname(f, extract_path, request, user):
    result, mod_name = extract_file(f, extract_path, request, user)
    if not result:
        return result, mod_name

    xml_path = os.path.join(extract_path, mod_name, "module.xml")
    # check that the module.xml file exists
    if not os.path.isfile(xml_path):
        msg_text = _(u"Zip file does not contain a module.xml file")
        messages.info(request, msg_text, extra_tags="danger")
        CoursePublishingLog(user=user,
                            action="no_module_xml",
                            data=msg_text).save()
        return False, 400

    # parse the module.xml file
    doc = ET.parse(xml_path)
    meta_info = parse_course_meta(doc)

    return True, meta_info['shortname']


def extract_file(f, extract_path, request, user):
    zipfilepath = os.path.join(settings.COURSE_UPLOAD_DIR, f.name)
    with open(zipfilepath, 'wb+') as destination:
        for chunk in f.chunks():
            destination.write(chunk)
    try:
        with ZipFile(zipfilepath) as zip_file:
            zip_file.extractall(path=extract_path)
            mod_name = ''

            top_level_file = {file.split('/')[0] for file in zip_file.namelist()}
            if len(top_level_file) == 1:
                top_level_filename = top_level_file.pop().split('/')[0]
                if os.path.isdir(os.path.join(extract_path, top_level_filename)):
                    mod_name = top_level_filename

    except (OSError, BadZipfile):
        msg_text = _(u"Invalid zip file")
        messages.error(request, msg_text, extra_tags="danger")
        CoursePublishingLog(user=user,
                            action="invalid_zip",
                            data=msg_text).save()
        shutil.rmtree(extract_path, ignore_errors=True)
        return False, 500

    return True, mod_name


def handle_uploaded_file(f, extract_path, request, user):
    result, mod_name = extract_file(f, extract_path, request, user)
    if not result:
        return result, mod_name, False

    # check there is at least a sub dir
    if mod_name == '':
        msg_text = _(u"Invalid zip file")
        messages.info(request, msg_text, extra_tags="danger")
        CoursePublishingLog(user=user,
                            action="invalid_zip",
                            data=msg_text).save()
        shutil.rmtree(extract_path, ignore_errors=True)
        return False, 400, False

    response = 200
    try:
        course, response, is_new_course = process_course(extract_path, f, mod_name, request, user)
    except Exception as e:
        logger.error(e)
        messages.error(request, str(e), extra_tags="danger")
        CoursePublishingLog(user=user,
                            action="upload_error",
                            data=str(e)).save()
        return False, 500, False
    finally:
        # remove the temp upload files
        shutil.rmtree(extract_path, ignore_errors=True)

    return course, response, is_new_course


def process_course(extract_path, f, mod_name, request, user):
    xml_path = os.path.join(extract_path, mod_name, "module.xml")
    # check that the module.xml file exists
    if not os.path.isfile(xml_path):
        msg_text = _(u"Zip file does not contain a module.xml file")
        messages.info(request, msg_text, extra_tags="danger")
        CoursePublishingLog(user=user,
                            action="no_module_xml",
                            data=msg_text).save()
        return False, 400, False

    # parse the module.xml file
    doc = ET.parse(xml_path)
    meta_info = parse_course_meta(doc)

    is_new_course = False
    oldsections = []
    old_course_filename = None
    old_course_version = None

    # Find if course already exists
    try:
        course = Course.objects.get(shortname=meta_info['shortname'])
        course_manager = CoursePermissions.objects.filter(
            user=user,
            course=course,
            role=CoursePermissions.MANAGER).count()
        # check that the current user is allowed to wipe out the other course
        if course.user != user and course_manager == 0:
            msg_text = \
                _(u"Sorry, you do not have permissions to update this course.")
            messages.info(request, msg_text)
            CoursePublishingLog(course=course,
                                new_version=meta_info['versionid'],
                                old_version=course.version,
                                user=user,
                                action="permissions_error",
                                data=msg_text).save()
            return False, 401, is_new_course
        # check if course version is older
        if course.version > meta_info['versionid']:
            msg_text = _(u"A newer version of this course already exists")
            messages.info(request, msg_text)
            CoursePublishingLog(course=course,
                                new_version=meta_info['versionid'],
                                old_version=course.version,
                                user=user,
                                action="newer_version_exists",
                                data=msg_text).save()
            return False, 400, is_new_course

        # obtain the old sections
        oldsections = list(Section.objects.filter(course=course)
                           .values_list('pk', flat=True))
        # wipe out old media
        oldmedia = Media.objects.filter(course=course)
        oldmedia.delete()

        old_course_filename = course.filename
        course.lastupdated_date = timezone.now()
        old_course_version = course.version
        result, error_msg = validate_course_status(course, request)
        if result is False:
            CoursePublishingLog(course=course,
                                new_version=meta_info['versionid'],
                                old_version=old_course_version,
                                user=user,
                                action="invalid_course_status",
                                data=error_msg).save()
            return result, 400, is_new_course

    except Course.DoesNotExist:
        course = Course()
        is_new_course = True

    course.status = request.POST['status']
    course.shortname = meta_info['shortname']
    course.title = meta_info['title']
    course.description = meta_info['description']
    course.version = meta_info['versionid']
    course.priority = int(meta_info['priority'])
    course.user = user
    course.filename = f.name
    course.save()

    if not parse_course_contents(request, doc, course, user, is_new_course):
        return False, 500, is_new_course
    clean_old_course(request, user, oldsections, old_course_filename, course)

    # save gamification events
    if 'gamification' in meta_info:
        events = parse_gamification_events(meta_info['gamification'])
        for event in events:
            # Only add events if the didn't exist previously
            e, created = CourseGamificationEvent.objects.get_or_create(
                course=course, event=event['name'],
                defaults={'points': event['points'], 'user': user})

            if created:
                msg_text = \
                    _(u'Gamification for "%(event)s" at course level added') \
                    % {'event': e.event}
                messages.info(request, msg_text)
                CoursePublishingLog(course=course,
                                    new_version=meta_info['versionid'],
                                    old_version=old_course_version,
                                    user=user,
                                    action="gamification_added",
                                    data=msg_text).save()

    tmp_path = replace_zip_contents(xml_path, doc, mod_name, extract_path)
    # Extract the final file into the courses area for preview
    zipfilepath = os.path.join(settings.COURSE_UPLOAD_DIR, f.name)
    shutil.copy(tmp_path + ".zip", zipfilepath)

    course_preview_path = os.path.join(settings.MEDIA_ROOT, "courses")
    ZipFile(zipfilepath).extractall(path=course_preview_path)

    writer = GamificationXMLWriter(course)
    writer.update_gamification(request.user)

    return course, 200, is_new_course


def process_course_sections(request, structure, course, user, is_new_course):
    for index, section in enumerate(structure.findall("section")):

        activities = section.find('activities')
        # Check if the section contains any activity
        # (to avoid saving an empty one)
        if activities is None or len(activities.findall('activity')) == 0:
            msg_text = _("Section ") \
                        + str(index + 1) \
                        + _(" does not contain any activities.")
            messages.info(request, msg_text)
            CoursePublishingLog(course=course,
                                user=user,
                                action="no_activities",
                                data=msg_text).save()
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
            parse_and_save_activity(request,
                                    user,
                                    course,
                                    section,
                                    act,
                                    is_new_course)


def process_course_media_events(request, media, events, course, user):
    for event in events:
        # Only add events if the didn't exist previously
        e, created = MediaGamificationEvent.objects \
            .get_or_create(media=media,
                           event=event['name'],
                           defaults={'points': event['points'],
                                     'user': request.user})

        if created:
            msg_text = _(u'Gamification for "%(event)s" at course \
                        level added') % {'event': e.event}
            messages.info(request, msg_text)
            CoursePublishingLog(course=course,
                                user=user,
                                action="course_gamification_added",
                                data=msg_text).save()


def process_course_media(request, media_element, course, user):
    for file_element in media_element.findall('file'):
        media = Media()
        media.course = course
        media.filename = file_element.get("filename")
        url = file_element.get("download_url")
        media.digest = file_element.get("digest")

        if len(url) > Media.URL_MAX_LENGTH:
            msg_text = _(u'File %(filename)s has a download URL larger \
                        than the maximum length permitted. The media file \
                        has not been registered, so it won\'t be tracked. \
                        Please, fix this issue and upload the course \
                        again.') % {'filename': media.filename}
            messages.info(request, msg_text)
            CoursePublishingLog(course=course,
                                user=user,
                                action="media_url_too_long",
                                data=msg_text).save()
        else:
            media.download_url = url
            # get any optional attributes
            for attr_name, attr_value in file_element.attrib.items():
                if attr_name == "length":
                    media.media_length = attr_value
                if attr_name == "filesize":
                    media.filesize = attr_value

            media.save()
            # save gamification events
            gamification = file_element.find('gamification')
            events = parse_gamification_events(gamification)

            process_course_media_events(request, media, events, course, user)


def parse_course_contents(request, xml_doc, course, user, is_new_course):

    # add in any baseline activities
    parse_baseline_activities(request, xml_doc, course, user, is_new_course)

    # add all the sections and activities
    structure = xml_doc.find("structure")
    if len(structure.findall("section")) == 0:
        course.delete()
        msg_text = \
            _(u"There don't appear to be any activities in this upload file.")
        messages.info(request, msg_text, extra_tags="danger")
        CoursePublishingLog(user=user,
                            action="no_activities",
                            data=msg_text).save()
        return False

    process_course_sections(request, structure, course, user, is_new_course)

    media_element = xml_doc.find('media')
    if media_element is not None:
        process_course_media(request, media_element, course, user)
    return True


def parse_baseline_activities(request, xml_doc, course, user, is_new_course):

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
                parse_and_save_activity(request,
                                        user,
                                        course,
                                        section,
                                        activity_node,
                                        is_new_course,
                                        is_baseline=True)


def get_activity_content(activity):
    content = ""
    activity_type = activity.get("type")
    if activity_type == "page" or activity_type == "url":
        temp_content = {}
        for t in activity.findall("location"):
            if t.text:
                temp_content[t.get('lang')] = t.text
        content = json.dumps(temp_content)
    elif activity_type == "quiz" or activity_type == "feedback":
        for c in activity.findall("content"):
            content = c.text
    elif activity_type == "resource":
        for c in activity.findall("location"):
            content = c.text
    else:
        content = None

    return content, activity_type


def parse_and_save_activity(request,
                            user,
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
    existed = False
    try:
        activity = Activity.objects.get(
            digest=digest, section__course__shortname=course.shortname)
        existed = True
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

    if not existed and not is_new_course:
        msg_text = _(u'Activity "%(act)s"(%(digest)s) did not exist \
                     previously.') % {'act': activity.title,
                                      'digest': activity.digest}
        messages.warning(request, msg_text)
        CoursePublishingLog(course=course,
                            user=user,
                            action="activity_added",
                            data=msg_text).save()
    else:
        msg_text = _(u'Activity "%(act)s"(%(digest)s) previously existed. \
                    Updated with new information') \
                    % {'act': activity.title,
                       'digest': activity.digest}
        '''
        If we also want to show the activities that previously existed,
        uncomment this next line
        messages.info(req, msg_text)
        '''
        CoursePublishingLog(course=course,
                            user=user,
                            action="activity_updated",
                            data=msg_text).save()

    if (activity_type == "quiz") or (activity_type == "feedback"):
        updated_json = parse_and_save_quiz(user, activity)
        # we need to update the JSON contents both in the XML and in the
        # activity data
        activity_node.find("content").text = \
            "<![CDATA[ " + updated_json + "]]>"
        activity.content = updated_json

    activity.save()

    # save gamification events
    gamification = activity_node.find('gamification')
    events = parse_gamification_events(gamification)
    for event in events:
        e, created = ActivityGamificationEvent.objects.get_or_create(
            activity=activity, event=event['name'],
            defaults={'points': event['points'], 'user': request.user})

        if created:
            msg_text = _(u'Gamification for "%(event)s" at activity \
                        "%(act)s"(%(digest)s) added') \
                      % {'event': e.event,
                         'act': activity.title,
                         'digest': activity.digest}
            messages.info(request, msg_text)
            CoursePublishingLog(course=course,
                                user=user,
                                action="activity_gamification_added",
                                data=msg_text).save()


def parse_and_save_quiz(user, activity):
    """
    Parses activity content that is a Quiz and saves it to the DB
    :param user: the user that uploaded the course
    :param activity: an activity object that contains the quiz as a json object
    :return: None
    """

    quiz_obj = json.loads(activity.content)
    quiz_existed = False
    course = activity.section.course
    # first of all, we find the quiz digest to see if it is already saved
    if quiz_obj['props']['digest']:
        quiz_digest = quiz_obj['props']['digest']

        try:
            quizzes = Quiz.objects.filter(quizprops__value=quiz_digest,
                                          quizprops__name=QuizProps.DIGEST,
                                          course=course) \
                                          .order_by('-id')
            quiz_existed = len(quizzes) > 0
            # remove any possible duplicate (possible scenario when
            # transitioning between export versions)
            for quiz in quizzes[1:]:
                quiz.delete()

        except Quiz.DoesNotExist:
            quiz_existed = False

    if quiz_existed:
        quiz = update_quiz(user, quizzes.first(), quiz_obj, course)
    else:
        quiz = create_quiz(user, quiz_obj, course)

    # add quiz props
    quiz_obj['id'] = quiz.pk
    create_or_update_quiz_props(quiz, quiz_obj)

    return json.dumps(quiz_obj)


def create_quiz(user, quiz_obj, course):
    quiz = Quiz()
    add_quiz_info(user, quiz, quiz_obj, course)

    # add quiz questions
    create_quiz_questions(user, quiz, quiz_obj)

    return quiz


def update_quiz(user, quiz, quiz_obj, course):
    add_quiz_info(user, quiz, quiz_obj, course)
    # If the quiz already existed (same digest) we can update the questions
    # based on its current titles, assuming they haven't changed
    update_quiz_questions(quiz, quiz_obj)

    return quiz


def get_content(elem, node_name):
    for node in elem.findall(node_name):
        return None if node is None else node.text
    return None


def parse_course_meta(xml_doc):

    meta_info = {'versionid': 0, 'shortname': ''}
    for meta in xml_doc.findall('meta')[:1]:
        meta_info['versionid'] = int(meta.find('versionid').text)

        meta_info['priority'] = int(meta.find('priority').text)

        title = {}
        for t in meta.findall('title'):
            title[t.get('lang')] = t.text
        meta_info['title'] = json.dumps(title)

        description = {}
        for t in meta.findall('description'):
            description[t.get('lang')] = t.text
        meta_info['description'] = json.dumps(description)

        meta_info['shortname'] = get_content(meta, 'shortname')
        exportversion = meta.find('exportversion')
        if exportversion is not None:
            meta_info['exportversion'] = exportversion
        meta_info['gamification'] = meta.find('gamification')

    return meta_info


def parse_gamification_events(element):
    events = []
    if element is not None:
        for e in element.findall("event"):
            event_name = e.get('name')
            points = e.text
            events.append({'name': event_name, 'points': points})
    return events


def replace_zip_contents(xml_path,
                         xml_doc,
                         mod_name,
                         dest,
                         encoding='utf-8'):

    with codecs.open(xml_path, mode="w", encoding=encoding) as fh:
        new_xml = ET.tostring(xml_doc.getroot(),
                              encoding=encoding).decode('utf-8')
        new_xml = unescape_xml(new_xml)
        fh.write("<?xml version='1.0' encoding='%s'?>\n" % encoding)
        fh.write(new_xml)

    tmp_zipfilepath = os.path.join(dest, 'tmp_course')
    shutil.make_archive(tmp_zipfilepath, 'zip', dest, base_dir=mod_name)
    return tmp_zipfilepath


def clean_old_course(req, user, oldsections, old_course_filename, course):
    for section in oldsections:
        sec = Section.objects.get(pk=section)
        for act in sec.activities():
            msg_text = _(u'Activity "%(act)s"(%(digest)s) is no longer in \
                        the course.') % {'act': act.title,
                                         'digest': act.digest}
            messages.info(req, msg_text)
            CoursePublishingLog(course=course,
                                user=user,
                                action="activity_removed",
                                data=msg_text).save()
        sec.delete()

    if old_course_filename is not None and old_course_filename != course.filename:
        try:
            os.remove(os.path.join(settings.COURSE_UPLOAD_DIR,
                                   old_course_filename))
        except OSError:
            pass


# helper functions
def create_or_update_quiz_props(quiz, quiz_obj):
    for prop in quiz_obj['props']:
        if prop != 'id':
            qprop, created = QuizProps.objects.get_or_create(quiz=quiz,
                                                             name=prop)
            qprop.value = quiz_obj['props'][prop]
            qprop.save()


def create_quiz_questions(user, quiz, quiz_obj):
    for q in quiz_obj['questions']:

        question = Question(owner=user,
                            type=q['question']['type'],
                            title=clean_lang_dict(q['question']['title']))

        question.save()

        quiz_question = QuizQuestion(quiz=quiz,
                                     question=question,
                                     order=q['order'])
        quiz_question.save()

        q['id'] = quiz_question.pk
        q['question']['id'] = question.pk

        for prop in q['question']['props']:
            if prop != 'id':
                QuestionProps(
                    question=question, name=prop,
                    value=q['question']['props'][prop]
                ).save()

        for r in q['question']['responses']:
            response = Response(
                owner=user,
                question=question,
                title=clean_lang_dict(r['title']),
                score=r['score'],
                order=r['order']
            )
            response.save()
            r['id'] = response.pk

            for prop in r['props']:
                if prop != 'id':
                    ResponseProps(
                        response=response, name=prop,
                        value=r['props'][prop]
                    ).save()


def add_quiz_info(user, quiz, quiz_obj, course):
    quiz.owner = user
    quiz.title = clean_lang_dict(quiz_obj['title'])
    quiz.description = clean_lang_dict(quiz_obj['description'])
    quiz.course = course
    quiz.save()


def update_quiz_questions(quiz, quiz_obj):
    for q in quiz_obj['questions']:
        question = Question.objects.filter(
            type=q['question']['type'],
            title=clean_lang_dict(q['question']['title']),
            quiz=quiz)

        if not question:
            question_prop = QuestionProps.objects.filter(name="moodle_question_id",
                                                         value=q['question']['props']['moodle_question_id']) \
                                                         .order_by('-id').first()

            if not question_prop:
                continue

            question_id = question_prop.question_id

            question = Question.objects.filter(id=question_id, quiz=quiz)

        qcount = question.count()
        if qcount == 0:
            continue
        elif qcount == 1:
            question = question.first()
        else:
            question = question.filter(quizquestion__order=q['order']).first()

        question.type = q['question']['type']
        question.title = clean_lang_dict(q['question']['title'])
        question.save()

        quiz_question, created = QuizQuestion.objects.update_or_create(
            quiz=quiz, question=question, defaults={'order': q['order']})
        q['id'] = quiz_question.pk
        q['question']['id'] = question.pk

        for prop in q['question']['props']:
            if prop != 'id':
                qprop, created = QuestionProps.objects.get_or_create(
                    question=question, name=prop)
                qprop.value = q['question']['props'][prop]
                qprop.save()


def validate_course_status(course, request):
    """
    When uploading an existing course:
      - If the course status is LIVE, upload the course and update status from the request.
      - If the course status is different than LIVE, only upload the course if the status matches the status from the
        request.
    """
    result = True
    error_msg = ""

    if (course.status in [CourseStatus.DRAFT,
                          CourseStatus.ARCHIVED,
                          CourseStatus.NEW_DOWNLOADS_DISABLED,
                          CourseStatus.READ_ONLY]
            and course.status != request.POST['status']):
        error_msg = f"This course currently has {course.status} status, so cannot now be updated."
        messages.info(request, error_msg)
        result = False

    return result, error_msg
