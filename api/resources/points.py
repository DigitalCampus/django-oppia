from django.conf.urls import url
from django.http import JsonResponse
from tastypie.authentication import ApiKeyAuthentication
from tastypie.authorization import ReadOnlyAuthorization
from tastypie.resources import ModelResource
from tastypie.utils import timezone

from oppia.models import Points


class PointsResource(ModelResource):
    class Meta:
        queryset = Points.objects.all().order_by('-date')
        allowed_methods = ['get']
        fields = ['date', 'description', 'points', 'type']
        resource_name = 'points'
        include_resource_uri = False
        authentication = ApiKeyAuthentication()
        authorization = ReadOnlyAuthorization()
        always_return_data = True

    def get_object_list(self, request):
        return super(PointsResource, self) \
            .get_object_list(request) \
            .filter(user=request.user)[:100]

    def dehydrate(self, bundle):
        bundle.data['date'] = bundle.data['date'].strftime("%Y-%m-%d %H:%M:%S")
        return bundle

    def prepend_urls(self):
        return [
            url(r"^leaderboard/$",
                self.wrap_view('leaderboard'),
                name="api_leaderboard"),
        ]

    def leaderboard(self, request, **kwargs):

        self.method_check(request, allowed=['get'])
        self.is_authenticated(request)
        self.throttle_check(request)

        if request.is_secure():
            prefix = 'https://'
        else:
            prefix = 'http://'

        response_data = {}
        response_data['generated_date'] = timezone.now()
        response_data['server'] = prefix + request.META['SERVER_NAME']
        leaderboard = Points.get_leaderboard()
        response_data['leaderboard'] = []

        for idx, leader in enumerate(leaderboard):
            leader_data = {}
            leader_data['position'] = idx + 1
            leader_data['username'] = leader.username
            leader_data['first_name'] = leader.first_name
            leader_data['last_name'] = leader.last_name
            leader_data['points'] = leader.total
            leader_data['badges'] = leader.badges
            response_data['leaderboard'].append(leader_data)

        return JsonResponse(response_data)
