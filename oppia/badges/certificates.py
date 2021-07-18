import datetime
import io
import qrcode
import uuid

from django.forms import ValidationError
from django.http import FileResponse
from django.shortcuts import render, reverse
from django.utils.translation import ugettext_lazy as _
from django.views.generic import TemplateView

from PIL import Image

from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4, landscape, portrait
from reportlab.lib.utils import ImageReader

from oppia.models import Award, Course, CertificateTemplate

from profile.models import CustomField, UserProfileCustomField

from settings import constants
from settings.models import SettingProperties


def generate_certificate_pdf(display_name,
                             certificate_template_id,
                             date,
                             validation_uuid):
    cert_template = CertificateTemplate.objects.get(pk=certificate_template_id)
    buffer = io.BytesIO()

    img = Image.open(cert_template.image_file.path)
    w, h = img.size

    # Create the PDF object
    if w > h:
        cert = canvas.Canvas(buffer, pagesize=landscape(A4))
    else:
        cert = canvas.Canvas(buffer, pagesize=portrait(A4))
    cert.setTitle(cert_template.course.get_title())

    # add background
    cert.drawImage(cert_template.image_file.path, 0, 0)

    # add name
    if cert_template.include_name:
        cert.setFont('Helvetica-Bold', 24)
        cert.drawCentredString(cert_template.name_x,
                               cert_template.name_y,
                               display_name)

    # add course
    if cert_template.include_course_title:
        cert.setFont('Helvetica-Bold', 24)
        cert.drawCentredString(cert_template.course_title_x,
                               cert_template.course_title_y,
                               cert_template.course.get_title())

    # add date
    if cert_template.include_date:
        cert.setFont('Helvetica-Bold', 16)
        cert.drawCentredString(cert_template.date_x,
                               cert_template.date_y,
                               date)

    host = SettingProperties.get_string(constants.OPPIA_HOSTNAME, '')
    url_path = reverse('oppia:certificate_validate',
                       args=[validation_uuid])

    validation_link = host + url_path

    # add url
    if cert_template.validation == CertificateTemplate.VALIDATION_OPTION_URL:
        cert.setFont('Helvetica', 10)
        cert.drawCentredString(cert_template.validation_x,
                               cert_template.validation_y,
                               "Verify certificate: " + validation_link)

    # add QR Code
    if cert_template.validation == \
            CertificateTemplate.VALIDATION_OPTION_QRCODE:
        qr_img = qrcode.make(validation_link)
        maxsize = (60, 60)
        qr_img.thumbnail(maxsize, Image.ANTIALIAS)

        bytes_in = io.BytesIO()
        qr_img.save(bytes_in, format='png')
        bytes_in.seek(0)
        qr = ImageReader(bytes_in)
        cert.drawImage(qr,
                       cert_template.validation_x,
                       cert_template.validation_y)
        cert.setFont('Helvetica', 10)
        cert.drawCentredString(cert_template.validation_x + 28,
                               cert_template.validation_y - 5,
                               (u"Verify Certificate"))

    cert.showPage()
    cert.save()
    return buffer
