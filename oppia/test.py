from django.contrib.auth.models import User
from django.test import TestCase, TransactionTestCase
from django.urls import reverse


class OppiaTestCase(TestCase):

    fixtures = ['tests/test_user.json',
                'tests/test_oppia.json',
                'tests/test_permissions.json',
                'tests/test_course_permissions.json',
                'tests/test_cohort.json']

    def setUp(self):
        super(OppiaTestCase, self).setUp()
        self.login_url = reverse('profile:login')
        self.admin_user = User.objects.get(pk=1)
        self.staff_user = User.objects.get(pk=3)
        self.teacher_user = User.objects.get(pk=4)
        self.normal_user = User.objects.get(pk=2)
        self.manager_user = User.objects.get(pk=5)
        self.viewer_user = User.objects.get(pk=6)
        self.unauthorized_template = "403.html"
        self.not_found_template = "404.html"

    def get_view(self, route, user=None):
        if user is not None:
            self.client.force_login(user)
        return self.client.get(route)


class OppiaTransactionTestCase(TransactionTestCase):

    fixtures = ['tests/test_user.json']

    def setUp(self):
        super(OppiaTransactionTestCase, self).setUp()
        self.login_url = reverse('profile:login')
        self.admin_user = User.objects.get(pk=1)
        self.staff_user = User.objects.get(pk=3)
        self.teacher_user = User.objects.get(pk=4)
        self.normal_user = User.objects.get(pk=2)
