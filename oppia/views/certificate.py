import io

from django.http import FileResponse
from django.views.generic import TemplateView

from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4, landscape

from oppia.models import CertificateTemplate


def generate_certificate_pdf(user, certificate_template_id, date):
    cert_template = CertificateTemplate.objects.get(pk=certificate_template_id)
    buffer = io.BytesIO()

    # Create the PDF object
    cert = canvas.Canvas(buffer, pagesize=landscape(A4))
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

    cert.showPage()
    cert.save()
    return buffer


class PreviewCertificateView(TemplateView):

    def get(self, request, certificate_template_id):

        buffer = generate_certificate_pdf(request.user,
                                          certificate_template_id,
                                          "14 May 2021")

        # FileResponse sets the Content-Disposition header so that browsers
        # present the option to save the file.
        buffer.seek(0)
        return FileResponse(buffer, filename='certificate.pdf')
