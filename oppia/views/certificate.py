import datetime
import io

from django.forms import ValidationError
from django.http import FileResponse
from django.shortcuts import render
from django.views.generic import TemplateView

from PIL import Image

from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4, landscape, portrait

from oppia.models import Award, CertificateTemplate


def generate_certificate_pdf(user, certificate_template_id, date):
    cert_template = CertificateTemplate.objects.get(pk=certificate_template_id)
    buffer = io.BytesIO()

    img = Image.open(cert_template.image_file.path)
    w,h = img.size
    
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
                               user.first_name + " " + user.last_name)

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
        
    # add url
    if cert_template.validation == 'URL':
        cert.setFont('Helvetica-Bold', 12)
        cert.drawCentredString(cert_template.validation_x,
                               cert_template.validation_y,
                               date)
    
    # add QR Code
    if cert_template.validation == 'QRCODE':
        pass

    cert.showPage()
    cert.save()
    return buffer


class PreviewCertificateView(TemplateView):

    def get(self, request, certificate_template_id):

        buffer = generate_certificate_pdf(
            request.user,
            certificate_template_id,
            datetime.datetime.now().strftime("%d %b %Y"))

        # FileResponse sets the Content-Disposition header
        buffer.seek(0)
        return FileResponse(buffer, filename='certificate.pdf')

class ValidateCertificateView(TemplateView):

    def get(self, request, validation_guid):
        try:
            award = Award.objects.get(validation_guid=validation_guid)
        except (Award.DoesNotExist, ValidationError):
            return render(request, 'oppia/certificates/invalid.html',
                  {'validation_guid': validation_guid})