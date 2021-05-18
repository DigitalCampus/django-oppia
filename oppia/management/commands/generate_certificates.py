import datetime

from django.core.files.base import ContentFile
from django.core.management.base import BaseCommand
from django.db.models import Q

from oppia.models import Award, CertificateTemplate
from oppia.views.certificate import generate_certificate_pdf


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
                                                  date_str)
                buffer.seek(0)
                filename = "certificate-%s-%s.pdf" % (award.user.username,
                                                      ct.course.shortname)
                award.certificate_pdf.save(filename,
                                           ContentFile(buffer.getvalue()),
                                           save=True)
                award.save()
