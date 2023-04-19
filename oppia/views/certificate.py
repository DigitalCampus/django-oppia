import datetime
import uuid

from django.core.exceptions import ValidationError
from django.http import FileResponse
from django.views.generic import TemplateView, DetailView

from oppia.badges.certificates import generate_certificate_pdf
from oppia.models import Award, Course


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


class ValidateCertificateView(DetailView):
    pk_url_kwarg = 'validation_uuid'
    model = Award

    def get_object(self, queryset=None):
        try:
            return Award.objects.filter(validation_uuid=self.kwargs['validation_uuid']).first()
        except ValidationError:
            return None

    def get_template_names(self):
        if self.object:
            return 'oppia/certificates/valid.html'
        else:
            return 'oppia/certificates/invalid.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.object:
            context['course'] = Course.objects.filter(awardcourse__award=self.object).first()
            context['award'] = self.object
        else:
            context['validation_uuid'] = self.kwargs['validation_uuid']
        return context
