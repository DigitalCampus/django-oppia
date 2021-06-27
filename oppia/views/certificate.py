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

from oppia.badges.certificates import generate_certificate_pdf
from oppia.models import Award, Course, CertificateTemplate

from profile.models import CustomField, UserProfileCustomField

from settings import constants
from settings.models import SettingProperties
    

class PreviewCertificateView(TemplateView):

    def get(self, request, certificate_template_id):

        buffer = generate_certificate_pdf(
            "** Name displays here **",
            certificate_template_id,
            datetime.datetime.now().strftime("%d %b %Y"),
            uuid.uuid4())

        # FileResponse sets the Content-Disposition header
        buffer.seek(0)
        return FileResponse(buffer, filename='certificate.pdf')


class ValidateCertificateView(TemplateView):

    def get(self, request, validation_uuid):
        try:
            award = Award.objects.get(validation_uuid=validation_uuid)
        except (Award.DoesNotExist, ValidationError):
            return render(request, 'oppia/certificates/invalid.html',
                  {'validation_uuid': validation_uuid})
        course = Course.objects.filter(awardcourse__award=award).first()
        return render(request, 'oppia/certificates/valid.html',
                  {'award': award,
                   'course': course})   
