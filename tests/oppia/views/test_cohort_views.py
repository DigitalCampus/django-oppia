from django.forms import ValidationError
from django.urls import reverse

from oppia.models import Cohort, Participant, CourseCohort
from oppia.test import OppiaTestCase
from oppia.views.cohort import cohort_add_roles, cohort_add_courses


class CohortViewsTest(OppiaTestCase):

    fixtures = ['tests/test_user.json',
                'tests/test_oppia.json',
                'tests/test_quiz.json',
                'tests/test_permissions.json',
                'tests/test_cohort.json',
                'tests/test_course_permissions.json']

    leaderboard_template = 'cohort/leaderboard.html'
    cohort_form_template = 'cohort/form.html'

    '''
    Leaderboard view
    '''
    def test_cohort_leaderboard_admin(self):
        self.client.force_login(self.admin_user)
        url = reverse('oppia:cohort_leaderboard', args=[1])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, self.leaderboard_template)

    def test_cohort_leaderboard_staff(self):
        self.client.force_login(self.staff_user)
        url = reverse('oppia:cohort_leaderboard', args=[1])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, self.leaderboard_template)

    def test_cohort_leaderboard_teacher_valid(self):
        self.client.force_login(self.teacher_user)
        url = reverse('oppia:cohort_leaderboard', args=[3])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, self.leaderboard_template)

    def test_cohort_leaderboard_teacher_invalid(self):
        self.client.force_login(self.teacher_user)
        url = reverse('oppia:cohort_leaderboard', args=[1])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 403)

    def test_cohort_leaderboard_admin_invalid_cohort(self):
        self.client.force_login(self.admin_user)
        url = reverse('oppia:cohort_leaderboard', args=[100])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)

    def test_cohort_leaderboard_admin_page123(self):
        self.client.force_login(self.admin_user)
        url = '%s?page=123' % reverse('oppia:cohort_leaderboard', args=[1])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, self.leaderboard_template)

    def test_cohort_leaderboard_admin_pageabc(self):
        self.client.force_login(self.admin_user)
        url = '%s?page=abc' % reverse('oppia:cohort_leaderboard', args=[1])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, self.leaderboard_template)

    '''
    add students, teachers, courses functions
    '''
    def test_cohort_add_students(self):
        cohort = Cohort.objects.get(pk=1)
        students = 'demo, admin, another'
        participant_count_start = \
            Participant.objects.filter(role=Participant.STUDENT).count()
        cohort_add_roles(cohort, Participant.STUDENT, students)
        participant_count_end = \
            Participant.objects.filter(role=Participant.STUDENT).count()
        self.assertEqual(participant_count_start+2, participant_count_end)

    def test_cohort_add_students_none(self):
        cohort = Cohort.objects.get(pk=1)
        students = ''
        participant_count_start = \
            Participant.objects.filter(role=Participant.STUDENT).count()

        cohort_add_roles(cohort, Participant.STUDENT, students)

        participant_count_end = \
            Participant.objects.filter(role=Participant.STUDENT).count()
        self.assertEqual(participant_count_start, participant_count_end)

    def test_cohort_add_courses(self):
        cohort = Cohort.objects.get(pk=1)
        courses = 'draft-test, ncd1-et, another'
        count_start = CourseCohort.objects.all().count()
        cohort_add_courses(cohort, courses)
        count_end = CourseCohort.objects.all().count()
        self.assertEqual(count_start+2, count_end)

    def test_cohort_add_courses_none(self):
        cohort = Cohort.objects.get(pk=1)
        courses = ''
        count_start = CourseCohort.objects.all().count()
        cohort_add_courses(cohort, courses)
        count_end = CourseCohort.objects.all().count()
        self.assertEqual(count_start, count_end)

    '''
    Cohort edit view - get
    '''
    def test_cohort_edit_get_admin(self):
        self.client.force_login(self.admin_user)
        url = reverse('oppia:cohort_edit', args=[1])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, self.cohort_form_template)

    def test_cohort_edit_get_staff(self):
        self.client.force_login(self.staff_user)
        url = reverse('oppia:cohort_edit', args=[1])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, self.cohort_form_template)

    def test_cohort_edit_get_teacher(self):
        self.client.force_login(self.teacher_user)
        url = reverse('oppia:cohort_edit', args=[3])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 403)

    def test_cohort_edit_get_user(self):
        self.client.force_login(self.normal_user)
        url = reverse('oppia:cohort_edit', args=[1])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 403)

    '''
    Cohort edit view - post
    '''
    def test_cohort_edit_post_valid(self):
        self.client.force_login(self.admin_user)
        url = reverse('oppia:cohort_edit', args=[1])
        data = {'start_date': '2020-01-01',
                'end_date': '2020-12-31',
                'description': 'Test cohort',
                'students': 'demo, staff',
                'teachers': 'teacher',
                'courses': 'draft-test, ncd1-et'}
        response = self.client.post(url, data)
        self.assertRedirects(response,
                             reverse('oppia:cohorts'),
                             302,
                             200)

    def test_cohort_edit_post_invalid_start_date(self):
        self.client.force_login(self.admin_user)
        url = reverse('oppia:cohort_edit', args=[1])
        data = {'start_date': '20-01',
                'end_date': '2020-12-35',
                'description': 'Test cohort',
                'students': 'demo, staff',
                'teachers': 'teacher',
                'courses': 'draft-test, ncd1-et'}
        self.client.post(url, data)
        self.assertRaises(ValidationError)

    def test_cohort_edit_post_invalid_end_date(self):
        self.client.force_login(self.admin_user)
        url = reverse('oppia:cohort_edit', args=[1])
        data = {'start_date': '2020-01-14',
                'end_date': '20-35',
                'description': 'Test cohort',
                'students': 'demo, staff',
                'teachers': 'teacher',
                'courses': 'draft-test, ncd1-et'}
        self.client.post(url, data)
        self.assertRaises(ValidationError)

    def test_cohort_edit_post_invalid_start_before_end_date(self):
        self.client.force_login(self.admin_user)
        url = reverse('oppia:cohort_edit', args=[1])
        data = {'start_date': '2020-01-14',
                'end_date': '2020-01-01',
                'description': 'Test cohort',
                'students': 'demo, staff',
                'teachers': 'teacher',
                'courses': 'draft-test, ncd1-et'}
        self.client.post(url, data)
        self.assertRaises(ValidationError)

    '''
    Cohort add view - post
    '''
    def test_cohort_add_post_valid(self):
        self.client.force_login(self.admin_user)
        url = reverse('oppia:cohort_add')
        data = {'start_date': '2020-01-01',
                'end_date': '2020-12-31',
                'description': 'my new cohort',
                'students': 'demo, staff',
                'teachers': 'teacher',
                'courses': 'draft-test, ncd1-et'}
        response = self.client.post(url, data)
        self.assertRedirects(response,
                             reverse('oppia:cohorts'),
                             302,
                             200)

    def test_cohort_add_post_invalid_dates(self):
        self.client.force_login(self.admin_user)
        url = reverse('oppia:cohort_add')
        data = {'start_date': '2020-01',
                'end_date': '2019-31',
                'description': 'my new cohort',
                'students': 'demo, staff',
                'teachers': 'teacher',
                'courses': 'draft-test, ncd1-et'}
        self.client.post(url, data)
        self.assertRaises(ValidationError)

    '''
    Cohort course view
    '''
    def test_cohort_course_invalid_course(self):
        self.client.force_login(self.admin_user)
        url = reverse('oppia:cohort_course_view', args=[3, 999])
        response = self.client.get(url)
        self.assertEqual(404, response.status_code)

    def test_cohort_course_inverse_order(self):
        self.client.force_login(self.admin_user)
        url = reverse('oppia:cohort_course_view', args=[3, 1])
        response = self.client.get('%s?order_by=-no_points' % url)
        self.assertEqual(200, response.status_code)

    def test_cohort_course_invalid_order(self):
        self.client.force_login(self.admin_user)
        url = reverse('oppia:cohort_course_view', args=[3, 1])
        response = self.client.get('%s?order_by=abcdef' % url)
        self.assertEqual(200, response.status_code)
