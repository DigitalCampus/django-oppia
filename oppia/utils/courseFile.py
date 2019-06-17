import os
import zipfile

import shutil

from django.conf import settings


def remove_from_zip(zipfname, temp_zip_path, course_shortname, *filenames):
    try:
        tempname = os.path.join(temp_zip_path, course_shortname +'.zip')
        with zipfile.ZipFile(zipfname, 'r') as zipread:
            with zipfile.ZipFile(tempname, 'w') as zipwrite:
                for item in zipread.infolist():
                    if item.filename not in filenames:
                        data = zipread.read(item.filename)
                        zipwrite.writestr(item, data)
        shutil.copy(tempname, zipfname)
    finally:
        shutil.rmtree(temp_zip_path)


def rewrite_xml_contents(user, course, xml_doc):
    temp_zip_path = os.path.join(settings.COURSE_UPLOAD_DIR, 'temp', str(user.id))
    module_xml = course.shortname + '/module.xml'
    try:
        os.makedirs(temp_zip_path)
    except OSError:
        pass  # leaf dir for user id already exists

    course_zip_file = os.path.join(settings.COURSE_UPLOAD_DIR, course.filename)
    remove_from_zip(course_zip_file, temp_zip_path, course.shortname, module_xml)

    xml_content = xml_doc.toprettyxml(indent='', newl='', encoding='utf-8')

    with zipfile.ZipFile(course_zip_file, 'a') as z:
        z.writestr(module_xml, xml_content)