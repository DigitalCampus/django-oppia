import datetime
import os

from django.core.files.base import ContentFile
from django.core.management.base import BaseCommand
from django.db.models import Q
from django.utils.translation import ugettext as _

from oppia import emailer
from oppia.models import Award, CertificateTemplate, Course
from oppia.views.certificate import generate_certificate_pdf

from settings import constants
from settings.models import SettingProperties


class Command(BaseCommand):
    help = 'Generate certificate files'

    def add_arguments(self, parser):

        # Optional argument to generate all certificates
        parser.add_argument(
            '--allcerts',
            dest='allcerts',
            action='store_true',
            help='generate for all certificates',
        )

    def handle(self, *args, **options):

        cert_templates = CertificateTemplate.objects.filter(enabled=True)

        # find the awards that haven't had certs generated
        for ct in cert_templates:
            awards = Award.objects.filter(awardcourse__course=ct.course)

            if not options['allcerts']:
                awards = awards.filter(
                     Q(certificate_pdf__isnull=True) | Q(certificate_pdf=""))

            for award in awards:
                print(award)
                date_str = award.award_date.strftime("%d %b %Y") 
                buffer = generate_certificate_pdf(award.user,
                                                  ct.id,
                                                  date_str,
                                                  award.validation_uuid)
                buffer.seek(0)
                filename = "certificate-%s-%s.pdf" % (award.user.username,
                                                      ct.course.shortname)
                award.certificate_pdf.save(filename,
                                           ContentFile(buffer.getvalue()),
                                           save=True)
                award.save()

                # Email certificate if enabled
                if SettingProperties.get_bool(
                        constants.OPPIA_EMAIL_CERTIFICATES, False):
                    self.email_certificate(award)
    
    def email_certificate(self, award):
        # check user has email address
        if award.user.email and not award.emailed:
            course = Course.objects.filter(awardcourse__award=award).first()
            
            emailer.send_oppia_email(
                    template_html='emails/certificate_awarded.html',
                    template_text='emails/certificate_awarded.txt',
                    subject=_(u"Certificate Awarded"),
                    fail_silently=False,
                    recipients=[award.user.email],
                    attachment_from_model=award.certificate_pdf.path,
                    award=award,
                    course=course
                    )
            award.emailed = True
            award.save()
