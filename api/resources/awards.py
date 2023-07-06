from django.conf import settings
from tastypie import fields
from tastypie.authentication import ApiKeyAuthentication
from tastypie.authorization import ReadOnlyAuthorization
from tastypie.resources import ModelResource

from api.resources.badges import BadgesResource
from api.serializers import PrettyJSONSerializer
from oppia.models import Award


class AwardsResource(ModelResource):
    badge = fields.ForeignKey(BadgesResource, 'badge', full=True, null=True)
    badge_icon = fields.CharField(attribute='_get_badge', readonly=True)

    class Meta:
        queryset = Award.objects.all().order_by('-award_date')
        allowed_methods = ['get']
        resource_name = 'awards'
        include_resource_uri = False
        serializer = PrettyJSONSerializer()
        authentication = ApiKeyAuthentication()
        authorization = ReadOnlyAuthorization()
        always_return_data = True

    def get_object_list(self, request):
        return super(AwardsResource, self).get_object_list(request).filter(user=request.user)

    def dehydrate_badge_icon(self, bundle):
        return bundle.request.build_absolute_uri(settings.MEDIA_URL + bundle.data['badge_icon'])

    def dehydrate(self, bundle):
        bundle.data['award_date'] = bundle.data['award_date'].strftime("%Y-%m-%d %H:%M:%S")
        return bundle
