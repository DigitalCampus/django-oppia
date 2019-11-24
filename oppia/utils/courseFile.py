import os
import zipfile

import shutil
from xml.sax.saxutils import unescape

from django.conf import settings


def remove_from_zip(zipfname, temp_zip_path, course_shortname, *filenames):
    try:
        tempname = os.path.join(temp_zip_path, course_shortname + '.zip')
        with zipfile.ZipFile(zipfname, 'r') as zipread:
            with zipfile.ZipFile(tempname, 'w') as zipwrite:
                for item in zipread.infolist():
                    if item.filename not in filenames:
                        data = zipread.read(item.filename)
                        zipwrite.writestr(item, data)
        shutil.copyfile(tempname, zipfname)
    finally:
        shutil.rmtree(temp_zip_path)


def unescape_xml(xml_content):
    new_xml = unescape(xml_content,
                       {"&apos;": "'", "&quot;": '"', "&nbsp;": " "})
    new_xml = new_xml.replace('&nbsp;', ' ') \
                     .replace('&quot;', '"') \
                     .replace('&', '&amp;')
    return new_xml


def rewrite_xml_contents(user, course, xml_doc):
    temp_zip_path = os.path.join(settings.COURSE_UPLOAD_DIR,
                                 'temp',
                                 str(user.id))
    module_xml = course.shortname + '/module.xml'
    try:
        os.makedirs(temp_zip_path)
    except OSError:
        pass  # leaf dir for user id already exists

    course_zip_file = os.path.join(settings.COURSE_UPLOAD_DIR,
                                   course.filename)
    remove_from_zip(course_zip_file,
                    temp_zip_path,
                    course.shortname,
                    module_xml)

    xml_content = xml_doc.toprettyxml(indent='',
                                      newl='',
                                      encoding='utf-8').decode('utf-8')
    xml_content = unescape_xml(xml_content)

    with zipfile.ZipFile(course_zip_file, 'a') as z:
        z.writestr(module_xml, xml_content)
