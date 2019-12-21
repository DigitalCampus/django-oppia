from django.urls import reverse
from oppia.test import OppiaTestCase
from oppia.views.cohort import cohort_add_roles, cohort_add_courses
from oppia.models import Course, Cohort, Participant, CourseCohort


class CohortViewsTest(OppiaTestCase):

    fixtures = ['tests/test_user.json',
                'tests/test_oppia.json',
                'tests/test_quiz.json',
                'tests/test_permissions.json',
                'tests/test_cohort.json']

    leaderboard_template = 'cohort/leaderboard.html'
    cohort_form_template = 'cohort/form.html'
    
    def test_cohort_leaderboard_admin(self):
        self.client.force_login(self.admin_user)
        url = reverse('oppia_cohort_leaderboard', args=[1])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, self.leaderboard_template)

    def test_cohort_leaderboard_staff(self):
        self.client.force_login(self.staff_user)
        url = reverse('oppia_cohort_leaderboard', args=[1])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, self.leaderboard_template)

    def test_cohort_leaderboard_teacher_valid(self):
        self.client.force_login(self.teacher_user)
        url = reverse('oppia_cohort_leaderboard', args=[3])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, self.leaderboard_template)
    
    def test_cohort_leaderboard_teacher_invalid(self):
        self.client.force_login(self.teacher_user)
        url = reverse('oppia_cohort_leaderboard', args=[1])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 403)
 
    def test_cohort_leaderboard_admin_invalid_cohort(self):
        self.client.force_login(self.admin_user)
        url = reverse('oppia_cohort_leaderboard', args=[100])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)

    def test_cohort_leaderboard_admin_page123(self):
        self.client.force_login(self.admin_user)
        url = '%s?page=123' % reverse('oppia_cohort_leaderboard', args=[1])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, self.leaderboard_template)

    def test_cohort_leaderboard_admin_pageabc(self):
        self.client.force_login(self.admin_user)
        url = '%s?page=abc' % reverse('oppia_cohort_leaderboard', args=[1])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, self.leaderboard_template)

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

    def test_cohort_edit_get_admin(self):
        self.client.force_login(self.admin_user)
        url = reverse('oppia_cohort_edit', args=[1])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, self.cohort_form_template)

    def test_cohort_edit_get_staff(self):
        self.client.force_login(self.staff_user)
        url = reverse('oppia_cohort_edit', args=[1])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, self.cohort_form_template)

    def test_cohort_edit_get_teacher(self):
        self.client.force_login(self.teacher_user)
        url = reverse('oppia_cohort_edit', args=[3])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 403)
    
    def test_cohort_edit_get_user(self):
        self.client.force_login(self.normal_user)
        url = reverse('oppia_cohort_edit', args=[1])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 403)
        