from django.test import TestCase
from tastypie.test import ResourceTestCaseMixin


class ActivityScheduleResourceTest(ResourceTestCaseMixin, TestCase):
    def setUp(self):
        super(ActivityScheduleResourceTest, self).setUp()

    # check get not allowed
    def test_get_not_found(self):
        self.assertHttpNotFound(self.api_client.get('/api/v1/activityschedule', format='json'))

    # check post not allowed
    def test_post_not_found(self):
        self.assertHttpNotFound(self.api_client.post('/api/v1/activityschedule', format='json', data={}))
