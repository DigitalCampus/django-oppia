
from django.contrib.auth.models import User
from django.utils.translation import ugettext_lazy as _

from tastypie import fields
from tastypie.authorization import Authorization
from tastypie.exceptions import BadRequest
from tastypie.resources import ModelResource

from oppia import emailer

from api.utils import check_required_params


class ResetPasswordResource(ModelResource):
    '''
    For resetting user password
    '''
    message = fields.CharField()

    class Meta:
        queryset = User.objects.all()
        resource_name = 'reset'
        allowed_methods = ['post']
        fields = ['username', 'message']
        authorization = Authorization()
        always_return_data = True
        include_resource_uri = False

    def obj_create(self, bundle, **kwargs):
        required = ['username', ]
        check_required_params(bundle, required)

        bundle.obj.username = bundle.data['username']
        try:
            user = User.objects.get(username__exact=bundle.obj.username)
        except User.DoesNotExist:
            try:
                user = User.objects.get(email__exact=bundle.obj.username)
            except User.DoesNotExist:
                raise BadRequest(_(u'Username/email not found'))

        newpass = User.objects.make_random_password(length=8)
        user.set_password(newpass)
        user.save()
        if bundle.request.is_secure():
            prefix = 'https://'
        else:
            prefix = 'http://'

        emailer.send_oppia_email(
                template_html='profile/email/password_reset.html',
                template_text='profile/email/password_reset.txt',
                subject="Password reset",
                fail_silently=False,
                recipients=[user.email],
                new_password=newpass,
                site=prefix + bundle.request.META['SERVER_NAME']
                )

        return bundle

    def dehydrate_message(self, bundle):
        message = _(u'An email has been sent to your registered email address \
                    with your new password')
        return message
