from django.contrib.auth.models import User
from django.utils.translation import ugettext_lazy as _

from tastypie import fields
from tastypie.authentication import Authentication
from tastypie.authorization import Authorization
from tastypie.exceptions import BadRequest
from tastypie.resources import ModelResource

from oppia import emailer


class UsernameResource(ModelResource):

    message = fields.CharField(readonly=True)

    class Meta:
        queryset = User.objects.all()
        resource_name = 'username'
        allowed_methods = ['post']
        fields = []
        authentication = Authentication()
        authorization = Authorization()
        always_return_data = True
        include_resource_uri = False

    def obj_create(self, bundle, **kwargs):

        if 'email' not in bundle.data or len(bundle.data['email']) == 0:
            raise BadRequest(_(u'Email missing'))

        email = bundle.data['email']

        user = User.objects.filter(email=email).first()

        if user is not None:
            emailer.send_oppia_email(
                    template_html='profile/email/username_reminder.html',
                    template_text='profile/email/username_reminder.txt',
                    subject="Username reminder",
                    fail_silently=False,
                    recipients=[user.email],
                    username=user.username,
                    )

        return bundle

    def dehydrate_message(self, bundle):
        return _(u'An email has been sent with a reminder of your username')
