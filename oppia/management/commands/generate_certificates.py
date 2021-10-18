
from django.contrib.auth.models import User
from django.core.files.base import ContentFile
from django.core.management.base import BaseCommand
from django.db.models import Q
from django.utils.translation import ugettext as _

from oppia import emailer
from oppia.models import Award, CertificateTemplate, Course
from oppia.badges.certificates import generate_certificate_pdf

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
            help='regenerate all certificates for all users',
        )

        # Optional argument to regenerate for individual user
        parser.add_argument(
            '--user',
            dest='user',
            type=int,
            help='regenerate all certificates for specific user',
        )

    def handle(self, *args, **options):

        cert_templates = CertificateTemplate.objects.filter(enabled=True)

        # find the awards that haven't had certs generated
        for ct in cert_templates:
            awards = Award.objects.filter(awardcourse__course=ct.course)

            if not options['allcerts'] and not options['user']:
                awards = awards.filter(
                     Q(certificate_pdf__isnull=True) | Q(certificate_pdf=""))
            elif options['user']:
                try:
                    user = User.objects.get(pk=options['user'])
                except User.DoesNotExist:
                    self.stdout.write("Invalid user id")
                    return
                awards = awards.filter(user=user)

            for award in awards:
                result = self.create_certificate(ct, award)

                # Email certificate if enabled
                if result and SettingProperties.get_bool(
                        constants.OPPIA_EMAIL_CERTIFICATES, False) \
                        and not options['allcerts']:
                    self.email_certificate(award)

    def create_certificate(self, ct, award):
        date_str = award.award_date.strftime("%d %b %Y")
        valid, display_name = ct.display_name(award.user)
        if not valid:
            return False
        buffer = generate_certificate_pdf(display_name,
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
        buffer.close()
        return True

    def email_certificate(self, award):
        # check user has email address
        course = Course.objects.filter(awardcourse__award=award).first()

        if award.user.email and not award.emailed:
            emailer.send_oppia_email(
                    template_html='emails/certificate_awarded.html',
                    template_text='emails/certificate_awarded.txt',
                    subject=_(u"Certificate Awarded"),
                    fail_silently=False,
                    recipients=[award.user.email],
                    attachment_from_model=award.certificate_pdf.path,
                    award=award,
                    course=course)
            award.emailed = True
            award.save()
        else:
            emailer.send_oppia_email(
                    template_html='emails/certificate_updated.html',
                    template_text='emails/certificate_updated.txt',
                    subject=_(u"Certificate updated"),
                    fail_silently=False,
                    recipients=[award.user.email],
                    attachment_from_model=award.certificate_pdf.path,
                    award=award,
                    course=course)
            award.emailed = True
            award.save()
