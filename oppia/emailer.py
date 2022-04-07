# oppia/emailer.py
from django.conf import settings
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.translation import gettext as _


def send_oppia_email(
        from_email=settings.SERVER_EMAIL,
        template_html=None,
        template_text=None,
        subject="",
        recipients=[],
        attachment_from_model=None,
        **context):
    """
    Base email task function

    Args:
        from_email: from address
        template_html: path to HTML body template
        template_text: path to text body template
        subject: email subject, not including prefex
        recipients: a list or iterable of email addresses
        **context: dictionary providing email template context

    Returns:
        0 or 1, return value of send_mail

    """
    email_subject = "[" + _('app_name') + "] " + subject
    text_content = render_to_string(template_text, context)
    html_content = render_to_string(template_html, context)
    mail = EmailMultiAlternatives(email_subject,
                                  text_content,
                                  from_email,
                                  recipients)
    mail.attach_alternative(html_content, "text/html")
    if attachment_from_model:
        mail.attach_file(attachment_from_model)
    return mail.send()
