from django.forms import ValidationError
from django.urls import reverse

from oppia.models import Cohort, Participant, CourseCohort, CohortCritera
from oppia.test import OppiaTestCase
from oppia.views.cohort import cohort_add_roles, cohort_add_courses


class CohortViewsTest(OppiaTestCase):

    fixtures = ['tests/test_user.json',
                'tests/test_oppia.json',
                'tests/test_customfields.json',
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
                'courses': 'draft-test, ncd1-et',
                'student-TOTAL_FORMS': 1,
                'student-INITIAL_FORMS': 0,
                'student-MIN_NUM_FORMS': 0,
                'student-MAX_NUM_FORMS': 1,
                'teacher-TOTAL_FORMS': 1,
                'teacher-INITIAL_FORMS': 0,
                'teacher-MIN_NUM_FORMS': 0,
                'teacher-MAX_NUM_FORMS': 1}
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
                'courses': 'draft-test, ncd1-et',
                'student-TOTAL_FORMS': 1,
                'student-INITIAL_FORMS': 0,
                'student-MIN_NUM_FORMS': 0,
                'student-MAX_NUM_FORMS': 1,
                'teacher-TOTAL_FORMS': 1,
                'teacher-INITIAL_FORMS': 0,
                'teacher-MIN_NUM_FORMS': 0,
                'teacher-MAX_NUM_FORMS': 1}
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

    def test_cohort_course_list_admin_can_view_all(self):
        self.client.force_login(self.admin_user)
        # We make the courses restricted
        for coursecohort in CourseCohort.objects.all():
            coursecohort.course.restricted = True
            coursecohort.course.save()
        url = reverse('oppia:course')
        response = self.client.get(url)
        self.assertEqual(200, response.status_code)
        self.assertEqual(response.context['paginator'].count, 4)

    def test_cohort_course_list_noncohort_user_cannot_view_restricted_courses(self):
        self.client.force_login(self.normal_user)
        # We make the courses restricted
        for coursecohort in CourseCohort.objects.all():
            coursecohort.course.restricted = True
            coursecohort.course.save()
        url = reverse('oppia:course')

        response = self.client.get(url)
        self.assertEqual(200, response.status_code)
        self.assertEqual(response.context['paginator'].count, 3)

        # We remove the user so does not belong to a cohort
        Participant.objects.filter(user=self.normal_user).delete()

        response = self.client.get(url)
        self.assertEqual(200, response.status_code)
        self.assertEqual(response.context['paginator'].count, 2)

    '''
    Cohort Criteria
    '''
    def test_add_matching_cohort_criteria_and_refresh(self):
        expected_students = [self.admin_user]  # admin_user.country='ES'
        expected_teachers = [self.teacher_user, self.normal_user] # teacher_user.country='FI' and normal_user.country='FI'

        # 1. Get cohort
        cohort = Cohort.objects.get(pk=2)
        cohort.criteria_based = True
        cohort.save()

        # 2. Add initial participants
        Participant(cohort=cohort, user=self.staff_user, role=Participant.STUDENT).save()

        # 3. Create matching cohort criteria
        CohortCritera(cohort=cohort, role=Participant.STUDENT, user_profile_field='country', user_profile_value='ES').save()
        CohortCritera(cohort=cohort, role=Participant.TEACHER, user_profile_field='country', user_profile_value='FI').save()

        # 4. Refresh cohort participants
        student_count, teacher_count = cohort.refresh_participants()

        # 5. Assert students and teachers are correct
        students = Participant.objects.filter(cohort=cohort, role=Participant.STUDENT)
        actual_students = [student.user for student in students]
        self.assertEqual(set(expected_students), set(actual_students))
        self.assertEqual(len(students), student_count)

        teachers = Participant.objects.filter(cohort=cohort, role=Participant.TEACHER)
        actual_teachers = [teacher.user for teacher in teachers]
        self.assertEqual(set(expected_teachers), set(actual_teachers))
        self.assertEqual(len(teachers), teacher_count)

        # 6. Assert initial participants are removed if they did not match the criteria
        self.assertTrue(self.staff_user not in actual_students)

    def test_add_non_matching_cohort_criteria_and_refresh(self):
        expected_students = []  # No users have 'NonExistingCountry' for country
        expected_teachers = []

        # 1. Get cohort
        cohort = Cohort.objects.get(pk=2)
        cohort.criteria_based = True
        cohort.save()

        # 2. Add initial participants
        Participant(cohort=cohort, user=self.staff_user, role=Participant.STUDENT).save()

        # 3. Create matching cohort criteria
        CohortCritera(cohort=cohort, role=Participant.STUDENT, user_profile_field='country', user_profile_value='NonExistingCountry').save()
        CohortCritera(cohort=cohort, role=Participant.TEACHER, user_profile_field='country', user_profile_value='NonExistingCountry').save()

        # 4. Refresh cohort participants
        student_count, teacher_count = cohort.refresh_participants()

        # 5. Assert students and teachers are correct
        students = Participant.objects.filter(cohort=cohort, role=Participant.STUDENT)
        actual_students = [student.user for student in students]
        self.assertEqual(set(expected_students), set(actual_students))
        self.assertEqual(len(students), student_count)

        teachers = Participant.objects.filter(cohort=cohort, role=Participant.TEACHER)
        actual_teachers = [teacher.user for teacher in teachers]
        self.assertEqual(set(expected_teachers), set(actual_teachers))
        self.assertEqual(len(teachers), teacher_count)

        # 6. Assert initial participants are removed if they did not match the criteria
        self.assertTrue(self.staff_user not in actual_students)

    def test_add_matching_cohort_criteria_and_update(self):
        expected_students = [self.staff_user, self.admin_user]  # staff_user.country=None and admin_user.country='ES'
        expected_teachers = [self.normal_user, self.teacher_user]  # normal_user.country='FI' and teacher_user.country='FI'

        # 1. Get cohort
        cohort = Cohort.objects.get(pk=2)
        cohort.criteria_based = True
        cohort.save()

        # 2. Add initial participants
        initial_students_count = 1
        Participant(cohort=cohort, user=self.staff_user, role=Participant.STUDENT).save()

        # 3. Create matching cohort criteria
        CohortCritera(cohort=cohort, role=Participant.STUDENT, user_profile_field='country', user_profile_value='ES').save()
        CohortCritera(cohort=cohort, role=Participant.TEACHER, user_profile_field='country', user_profile_value='FI').save()

        # 4. Update cohort participants
        updated_students, updated_teachers = cohort.update_participants()

        # 5. Assert students and teachers are correct
        students = Participant.objects.filter(cohort=cohort, role=Participant.STUDENT)
        actual_students = [student.user for student in students]
        self.assertEqual(set(expected_students), set(actual_students))
        self.assertEqual(len(students) - initial_students_count, updated_students)

        teachers = Participant.objects.filter(cohort=cohort, role=Participant.TEACHER)
        actual_teachers = [teacher.user for teacher in teachers]
        self.assertEqual(set(expected_teachers), set(actual_teachers))
        self.assertEqual(len(teachers), updated_teachers)

        # 6. Assert initial participants are kept in the cohort when updating even if they did not match the criteria
        self.assertTrue(self.staff_user in actual_students)

    def test_add_non_matching_cohort_criteria_and_update(self):
        expected_students = [self.normal_user]  # normal_user.country='FI' and admin_user.country='ES'
        expected_teachers = [self.teacher_user]  # staff_user.country='FI'

        # 1. Get cohort
        cohort = Cohort.objects.get(pk=2)
        cohort.criteria_based = True
        cohort.save()

        # 2. Add initial participants
        initial_students_count = 1
        initial_teachers_count = 1
        Participant(cohort=cohort, user=self.normal_user, role=Participant.STUDENT).save()
        Participant(cohort=cohort, user=self.teacher_user, role=Participant.TEACHER).save()

        # 3. Create matching cohort criteria
        CohortCritera(cohort=cohort, role=Participant.STUDENT, user_profile_field='country', user_profile_value='NonExistingCountry').save()
        CohortCritera(cohort=cohort, role=Participant.TEACHER, user_profile_field='country', user_profile_value='NonExistingCountry').save()

        # 4. Update cohort participants
        updated_students, updated_teachers = cohort.update_participants()

        # 5. Assert students and teachers are correct
        students = Participant.objects.filter(cohort=cohort, role=Participant.STUDENT)
        actual_students = [student.user for student in students]
        self.assertEqual(set(expected_students), set(actual_students))
        self.assertEqual(len(students) - initial_students_count, updated_students)

        teachers = Participant.objects.filter(cohort=cohort, role=Participant.TEACHER)
        actual_teachers = [teacher.user for teacher in teachers]
        self.assertEqual(set(expected_teachers), set(actual_teachers))
        self.assertEqual(len(teachers) - initial_teachers_count, updated_teachers)

        # 6. Assert initial participants are kept in the cohort when updating even if they did not match the criteria
        self.assertTrue(self.normal_user in actual_students)
        self.assertTrue(self.teacher_user in actual_teachers)

    def test_add_multiple_matching_cohort_criteria_and_refresh(self):
        expected_students = [self.normal_user]  # normal_user.country='FI' && normal_user.age=30
        expected_teachers = [self.teacher_user]  # teacher_user.country='FI' && teacher_user.age=40

        # 1. Get cohort
        cohort = Cohort.objects.get(pk=2)
        cohort.criteria_based = True
        cohort.save()

        # 2. Add initial participants
        Participant(cohort=cohort, user=self.admin_user, role=Participant.STUDENT).save()

        # 3. Create matching cohort criteria
        CohortCritera(cohort=cohort, role=Participant.STUDENT, user_profile_field='country', user_profile_value='FI').save()
        CohortCritera(cohort=cohort, role=Participant.STUDENT, user_profile_field='age', user_profile_value=30).save()
        CohortCritera(cohort=cohort, role=Participant.TEACHER, user_profile_field='country', user_profile_value='FI').save()
        CohortCritera(cohort=cohort, role=Participant.TEACHER, user_profile_field='age', user_profile_value=40).save()

        # 4. Refresh cohort participants
        student_count, teacher_count = cohort.refresh_participants()

        # 5. Assert students and teachers are correct
        students = Participant.objects.filter(cohort=cohort, role=Participant.STUDENT)
        actual_students = [student.user for student in students]
        self.assertEqual(set(expected_students), set(actual_students))
        self.assertEqual(len(students), student_count)

        teachers = Participant.objects.filter(cohort=cohort, role=Participant.TEACHER)
        actual_teachers = [teacher.user for teacher in teachers]
        self.assertEqual(set(expected_teachers), set(actual_teachers))
        self.assertEqual(len(teachers), teacher_count)

        # 6. Assert initial participants are removed if they did not match the criteria
        self.assertTrue(self.admin_user not in actual_students)

    def test_add_multiple_non_matching_cohort_criteria_and_refresh(self):
        expected_students = []  # No student having country='ES' and age=30
        expected_teachers = []  # No teacher having country='ES' and age=40

        # 1. Get cohort
        cohort = Cohort.objects.get(pk=2)
        cohort.criteria_based = True
        cohort.save()

        # 2. Add initial participants
        Participant(cohort=cohort, user=self.admin_user, role=Participant.STUDENT).save()

        # 3. Create matching cohort criteria
        CohortCritera(cohort=cohort, role=Participant.STUDENT, user_profile_field='country', user_profile_value='ES').save()
        CohortCritera(cohort=cohort, role=Participant.STUDENT, user_profile_field='age', user_profile_value=30).save()
        CohortCritera(cohort=cohort, role=Participant.TEACHER, user_profile_field='country', user_profile_value='ES').save()
        CohortCritera(cohort=cohort, role=Participant.TEACHER, user_profile_field='age', user_profile_value=40).save()

        # 4. Refresh cohort participants
        student_count, teacher_count = cohort.refresh_participants()

        # 5. Assert students and teachers are correct
        students = Participant.objects.filter(cohort=cohort, role=Participant.STUDENT)
        actual_students = [student.user for student in students]
        self.assertEqual(set(expected_students), set(actual_students))
        self.assertEqual(len(students), student_count)

        teachers = Participant.objects.filter(cohort=cohort, role=Participant.TEACHER)
        actual_teachers = [teacher.user for teacher in teachers]
        self.assertEqual(set(expected_teachers), set(actual_teachers))
        self.assertEqual(len(teachers), teacher_count)

        # 6. Assert initial participants are removed if they did not match the criteria
        self.assertTrue(self.admin_user not in actual_students)

    def test_add_multiple_matching_cohort_criteria_and_update(self):
        expected_students = [self.admin_user, self.normal_user]  # normal_user.country='FI' && normal_user.age=30
        expected_teachers = [self.admin_user, self.teacher_user] # teacher_user.country='FI' && teacher_user.age=40

        # 1. Get cohort
        cohort = Cohort.objects.get(pk=2)
        cohort.criteria_based = True
        cohort.save()

        # 2. Add initial participants
        initial_students_count = 1
        initial_teachers_count = 1
        Participant(cohort=cohort, user=self.admin_user, role=Participant.STUDENT).save()
        Participant(cohort=cohort, user=self.admin_user, role=Participant.TEACHER).save()

        # 3. Create matching cohort criteria
        CohortCritera(cohort=cohort, role=Participant.STUDENT, user_profile_field='country', user_profile_value='FI').save()
        CohortCritera(cohort=cohort, role=Participant.STUDENT, user_profile_field='age', user_profile_value=30).save()
        CohortCritera(cohort=cohort, role=Participant.TEACHER, user_profile_field='country', user_profile_value='FI').save()
        CohortCritera(cohort=cohort, role=Participant.TEACHER, user_profile_field='age', user_profile_value=40).save()

        # 4. Refresh cohort participants
        student_count, teacher_count = cohort.update_participants()

        # 5. Assert students and teachers are correct
        students = Participant.objects.filter(cohort=cohort, role=Participant.STUDENT)
        actual_students = [student.user for student in students]
        self.assertEqual(set(expected_students), set(actual_students))
        self.assertEqual(len(students) - initial_students_count, student_count)

        teachers = Participant.objects.filter(cohort=cohort, role=Participant.TEACHER)
        actual_teachers = [teacher.user for teacher in teachers]
        self.assertEqual(set(expected_teachers), set(actual_teachers))
        self.assertEqual(len(teachers) - initial_teachers_count, teacher_count)

        # 6. Assert initial participants are kept in the cohort when updating even if they did not match the criteria
        self.assertTrue(self.admin_user in actual_students)
        self.assertTrue(self.admin_user in actual_teachers)

    def test_add_multiple_non_matching_cohort_criteria_and_update(self):
        expected_students = [self.admin_user]  # No student having country='ES' and age=30. admin_user was already in the cohort
        expected_teachers = [self.admin_user]  # No teacher having country='ES' and age=40. admin_user was already in the cohort

        # 1. Get cohort
        cohort = Cohort.objects.get(pk=2)
        cohort.criteria_based = True
        cohort.save()

        # 2. Add initial participants
        initial_students_count = 1
        initial_teachers_count = 1
        Participant(cohort=cohort, user=self.admin_user, role=Participant.STUDENT).save()
        Participant(cohort=cohort, user=self.admin_user, role=Participant.TEACHER).save()

        # 3. Create matching cohort criteria
        CohortCritera(cohort=cohort, role=Participant.STUDENT, user_profile_field='country', user_profile_value='ES').save()
        CohortCritera(cohort=cohort, role=Participant.STUDENT, user_profile_field='age', user_profile_value=30).save()
        CohortCritera(cohort=cohort, role=Participant.TEACHER, user_profile_field='country', user_profile_value='ES').save()
        CohortCritera(cohort=cohort, role=Participant.TEACHER, user_profile_field='age', user_profile_value=40).save()

        # 4. Refresh cohort participants
        student_count, teacher_count = cohort.update_participants()

        # 5. Assert students and teachers are correct
        students = Participant.objects.filter(cohort=cohort, role=Participant.STUDENT)
        actual_students = [student.user for student in students]
        self.assertEqual(set(expected_students), set(actual_students))
        self.assertEqual(len(students) - initial_students_count, student_count)

        teachers = Participant.objects.filter(cohort=cohort, role=Participant.TEACHER)
        actual_teachers = [teacher.user for teacher in teachers]
        self.assertEqual(set(expected_teachers), set(actual_teachers))
        self.assertEqual(len(teachers) - initial_teachers_count, teacher_count)

        # 6. Assert initial participants are kept in the cohort when updating even if they did not match the criteria
        self.assertTrue(self.admin_user in actual_students)
        self.assertTrue(self.admin_user in actual_teachers)

    def test_add_matching_cohort_criteria_with_multiple_conditions_and_refresh(self):
        expected_students = [self.teacher_user, self.admin_user, self.normal_user]
        expected_teachers = [self.teacher_user, self.admin_user, self.normal_user]

        # 1. Get cohort
        cohort = Cohort.objects.get(pk=2)
        cohort.criteria_based = True
        cohort.save()

        # 2. Add initial participants
        Participant(cohort=cohort, user=self.staff_user, role=Participant.STUDENT).save()

        # 3. Create matching cohort criteria
        CohortCritera(cohort=cohort, role=Participant.STUDENT, user_profile_field='country', user_profile_value='ES,FI').save()
        CohortCritera(cohort=cohort, role=Participant.TEACHER, user_profile_field='country', user_profile_value='ES,FI').save()

        # 4. Refresh cohort participants
        student_count, teacher_count = cohort.refresh_participants()

        # 5. Assert students and teachers are correct
        students = Participant.objects.filter(cohort=cohort, role=Participant.STUDENT)
        actual_students = [student.user for student in students]
        self.assertEqual(set(expected_students), set(actual_students))
        self.assertEqual(len(students), student_count)

        teachers = Participant.objects.filter(cohort=cohort, role=Participant.TEACHER)
        actual_teachers = [teacher.user for teacher in teachers]
        self.assertEqual(set(expected_teachers), set(actual_teachers))
        self.assertEqual(len(teachers), teacher_count)

        # 6. Assert initial participants are removed if they did not match the criteria
        self.assertTrue(self.staff_user not in actual_students)
        self.assertTrue(self.staff_user not in actual_teachers)

    def test_add_non_matching_cohort_criteria_with_multiple_conditions_and_refresh(self):
        expected_students = [self.admin_user]  # admin_user.country='ES' and No users have 'NonExistingCountry' for country
        expected_teachers = [self.teacher_user, self.normal_user]  # teacher_user.country='FI' and normal_user.country='FI'

        # 1. Get cohort
        cohort = Cohort.objects.get(pk=2)
        cohort.criteria_based = True
        cohort.save()

        # 2. Add initial participants
        Participant(cohort=cohort, user=self.normal_user, role=Participant.STUDENT).save()

        # 3. Create matching cohort criteria
        CohortCritera(cohort=cohort, role=Participant.STUDENT, user_profile_field='country', user_profile_value='ES,NonExistingCountry').save()
        CohortCritera(cohort=cohort, role=Participant.TEACHER, user_profile_field='country', user_profile_value='FI,NonExistingCountry').save()

        # 4. Refresh cohort participants
        student_count, teacher_count = cohort.refresh_participants()

        # 5. Assert students and teachers are correct
        students = Participant.objects.filter(cohort=cohort, role=Participant.STUDENT)
        actual_students = [student.user for student in students]
        self.assertEqual(set(expected_students), set(actual_students))
        self.assertEqual(len(students), student_count)

        teachers = Participant.objects.filter(cohort=cohort, role=Participant.TEACHER)
        actual_teachers = [teacher.user for teacher in teachers]
        self.assertEqual(set(expected_teachers), set(actual_teachers))
        self.assertEqual(len(teachers), teacher_count)

        # 6. Assert initial participants are removed if they did not match the criteria
        self.assertTrue(self.normal_user not in actual_students)

    def test_add_matching_cohort_criteria_with_multiple_conditions_and_update(self):
        expected_students = [self.staff_user, self.teacher_user, self.admin_user, self.normal_user]
        expected_teachers = [self.teacher_user, self.admin_user, self.normal_user]

        # 1. Get cohort
        cohort = Cohort.objects.get(pk=2)
        cohort.criteria_based = True
        cohort.save()

        # 2. Add initial participants
        Participant(cohort=cohort, user=self.staff_user, role=Participant.STUDENT).save()

        # 3. Create matching cohort criteria
        CohortCritera(cohort=cohort, role=Participant.STUDENT, user_profile_field='country', user_profile_value='ES,FI').save()
        CohortCritera(cohort=cohort, role=Participant.TEACHER, user_profile_field='country', user_profile_value='ES,FI').save()

        # 4. Update cohort participants
        initial_students_count = 1
        student_count, teacher_count = cohort.update_participants()

        # 5. Assert students and teachers are correct
        students = Participant.objects.filter(cohort=cohort, role=Participant.STUDENT)
        actual_students = [student.user for student in students]
        self.assertEqual(set(expected_students), set(actual_students))
        self.assertEqual(len(students) - initial_students_count, student_count)

        teachers = Participant.objects.filter(cohort=cohort, role=Participant.TEACHER)
        actual_teachers = [teacher.user for teacher in teachers]
        self.assertEqual(set(expected_teachers), set(actual_teachers))
        self.assertEqual(len(teachers), teacher_count)

        # 6. Assert initial participants are kept in the cohort when updating even if they did not match the criteria
        self.assertTrue(self.staff_user in actual_students)

    def test_add_non_matching_cohort_criteria_with_multiple_conditions_and_update(self):
        expected_students = [self.normal_user]  # No users have 'NonExistingCountry' for country
        expected_teachers = []

        # 1. Get cohort
        cohort = Cohort.objects.get(pk=2)
        cohort.criteria_based = True
        cohort.save()

        # 2. Add initial participants
        Participant(cohort=cohort, user=self.normal_user, role=Participant.STUDENT).save()

        # 3. Create matching cohort criteria
        CohortCritera(cohort=cohort, role=Participant.STUDENT, user_profile_field='country', user_profile_value='NonExistingCountry1, NonExistingCountry2').save()

        # 4. Refresh cohort participants
        initial_students_count = 1
        student_count, teacher_count = cohort.update_participants()

        # 5. Assert students and teachers are correct
        students = Participant.objects.filter(cohort=cohort, role=Participant.STUDENT)
        actual_students = [student.user for student in students]
        self.assertEqual(set(expected_students), set(actual_students))
        self.assertEqual(len(students) - initial_students_count, student_count)

        teachers = Participant.objects.filter(cohort=cohort, role=Participant.TEACHER)
        actual_teachers = [teacher.user for teacher in teachers]
        self.assertEqual(set(expected_teachers), set(actual_teachers))
        self.assertEqual(len(teachers), teacher_count)

        # 6. Assert initial participants are kept in the cohort when updating even if they did not match the criteria
        self.assertTrue(self.normal_user in actual_students)

    def test_add_cohort_criteria_for_non_existing_field_and_refresh(self):
        expected_students = []  # No users have 'NonExistingCountry' for country
        expected_teachers = []

        # 1. Get cohort
        cohort = Cohort.objects.get(pk=2)
        cohort.criteria_based = True
        cohort.save()

        # 2. Add initial participants
        Participant(cohort=cohort, user=self.staff_user, role=Participant.STUDENT).save()

        # 3. Create matching cohort criteria
        CohortCritera(cohort=cohort, role=Participant.STUDENT, user_profile_field='NonExistingField', user_profile_value='ES').save()
        CohortCritera(cohort=cohort, role=Participant.TEACHER, user_profile_field='NonExistingField', user_profile_value='FI').save()

        # 4. Refresh cohort participants
        student_count, teacher_count = cohort.refresh_participants()

        # 5. Assert students and teachers are correct
        students = Participant.objects.filter(cohort=cohort, role=Participant.STUDENT)
        actual_students = [student.user for student in students]
        self.assertEqual(set(expected_students), set(actual_students))
        self.assertEqual(len(students), student_count)

        teachers = Participant.objects.filter(cohort=cohort, role=Participant.TEACHER)
        actual_teachers = [teacher.user for teacher in teachers]
        self.assertEqual(set(expected_teachers), set(actual_teachers))
        self.assertEqual(len(teachers), teacher_count)

        # 6. Assert initial participants are removed if they did not match the criteria
        self.assertTrue(self.staff_user not in actual_students)

    def test_add_cohort_criteria_for_non_existing_field_and_update(self):
        expected_students = [self.staff_user]  # No users have 'NonExistingCountry' for country
        expected_teachers = []

        # 1. Get cohort
        cohort = Cohort.objects.get(pk=2)
        cohort.criteria_based = True
        cohort.save()

        # 2. Add initial participants
        initial_students_count = 1
        Participant(cohort=cohort, user=self.staff_user, role=Participant.STUDENT).save()

        # 3. Create matching cohort criteria
        CohortCritera(cohort=cohort, role=Participant.STUDENT, user_profile_field='NonExistingField', user_profile_value='ES').save()
        CohortCritera(cohort=cohort, role=Participant.TEACHER, user_profile_field='NonExistingField', user_profile_value='FI').save()

        # 4. Refresh cohort participants
        student_count, teacher_count = cohort.update_participants()

        # 5. Assert students and teachers are correct
        students = Participant.objects.filter(cohort=cohort, role=Participant.STUDENT)
        actual_students = [student.user for student in students]
        self.assertEqual(set(expected_students), set(actual_students))
        self.assertEqual(len(students) - initial_students_count, student_count)

        teachers = Participant.objects.filter(cohort=cohort, role=Participant.TEACHER)
        actual_teachers = [teacher.user for teacher in teachers]
        self.assertEqual(set(expected_teachers), set(actual_teachers))
        self.assertEqual(len(teachers), teacher_count)

        # 6. Assert initial participants are kept in the cohort when updating even if they did not match the criteria
        self.assertTrue(self.staff_user in actual_students)

    def test_dont_refresh_cohort_if_no_criteria_set(self):
        expected_students = [self.normal_user]
        expected_teachers = [self.normal_user]

        # 1. Get cohort
        cohort = Cohort.objects.get(pk=2)
        cohort.criteria_based = True
        cohort.save()

        # 2. Add initial participants
        initial_students_count = 1
        initial_teachers_count = 1
        Participant(cohort=cohort, user=self.normal_user, role=Participant.STUDENT).save()
        Participant(cohort=cohort, user=self.normal_user, role=Participant.TEACHER).save()

        # 3. Refresh cohort participants
        student_count, teacher_count = cohort.refresh_participants()

        # 4. Assert students and teachers are correct
        students = Participant.objects.filter(cohort=cohort, role=Participant.STUDENT)
        actual_students = [student.user for student in students]
        self.assertEqual(set(expected_students), set(actual_students))
        self.assertEqual(len(students) - initial_students_count, student_count)

        teachers = Participant.objects.filter(cohort=cohort, role=Participant.TEACHER)
        actual_teachers = [teacher.user for teacher in teachers]
        self.assertEqual(set(expected_teachers), set(actual_teachers))
        self.assertEqual(len(teachers) - initial_teachers_count, teacher_count)

    def test_dont_update_cohort_if_no_criteria_set(self):
        expected_students = [self.normal_user]
        expected_teachers = [self.normal_user]

        # 1. Get cohort
        cohort = Cohort.objects.get(pk=2)
        cohort.criteria_based = True
        cohort.save()

        # 2. Add initial participants
        initial_students_count = 1
        initial_teachers_count = 1
        Participant(cohort=cohort, user=self.normal_user, role=Participant.STUDENT).save()
        Participant(cohort=cohort, user=self.normal_user, role=Participant.TEACHER).save()

        # 3. Refresh cohort participants
        student_count, teacher_count = cohort.update_participants()

        # 4. Assert students and teachers are correct
        students = Participant.objects.filter(cohort=cohort, role=Participant.STUDENT)
        actual_students = [student.user for student in students]
        self.assertEqual(set(expected_students), set(actual_students))
        self.assertEqual(len(students) - initial_students_count, student_count)

        teachers = Participant.objects.filter(cohort=cohort, role=Participant.TEACHER)
        actual_teachers = [teacher.user for teacher in teachers]
        self.assertEqual(set(expected_teachers), set(actual_teachers))
        self.assertEqual(len(teachers) - initial_teachers_count, teacher_count)

    def test_dont_refresh_cohort_if_criteria_based_is_false(self):
        expected_students = [self.normal_user]  # normal_user.country='FI'
        expected_teachers = [self.normal_user]

        # 1. Get cohort
        cohort = Cohort.objects.get(pk=2)
        cohort.criteria_based = False
        cohort.save()

        # 2. Add initial participants
        initial_students_count = 1
        initial_teachers_count = 1
        Participant(cohort=cohort, user=self.normal_user, role=Participant.STUDENT).save()
        Participant(cohort=cohort, user=self.normal_user, role=Participant.TEACHER).save()

        # 3. Create matching cohort criteria
        CohortCritera(cohort=cohort, role=Participant.STUDENT, user_profile_field='country', user_profile_value='ES').save()

        # 4. Refresh cohort participants
        student_count, teacher_count = cohort.refresh_participants()

        # 5. Assert students and teachers are correct
        students = Participant.objects.filter(cohort=cohort, role=Participant.STUDENT)
        actual_students = [student.user for student in students]
        self.assertEqual(set(expected_students), set(actual_students))
        self.assertEqual(len(students) - initial_students_count, student_count)

        teachers = Participant.objects.filter(cohort=cohort, role=Participant.TEACHER)
        actual_teachers = [teacher.user for teacher in teachers]
        self.assertEqual(set(expected_teachers), set(actual_teachers))
        self.assertEqual(len(teachers) - initial_teachers_count, teacher_count)

    def test_dont_update_cohort_if_criteria_based_is_false(self):
        expected_students = [self.normal_user]  # normal_user.country='FI'
        expected_teachers = [self.normal_user]

        # 1. Get cohort
        cohort = Cohort.objects.get(pk=2)
        cohort.criteria_based = False
        cohort.save()

        # 2. Add initial participants
        initial_students_count = 1
        initial_teachers_count = 1
        Participant(cohort=cohort, user=self.normal_user, role=Participant.STUDENT).save()
        Participant(cohort=cohort, user=self.normal_user, role=Participant.TEACHER).save()

        # 3. Create matching cohort criteria
        CohortCritera(cohort=cohort, role=Participant.STUDENT, user_profile_field='country', user_profile_value='ES').save()

        # 4. Update cohort participants
        updated_students, updated_teachers = cohort.update_participants()

        # 5. Assert students and teachers are correct
        students = Participant.objects.filter(cohort=cohort, role=Participant.STUDENT)
        actual_students = [student.user for student in students]
        self.assertEqual(set(expected_students), set(actual_students))
        self.assertEqual(len(students) - initial_students_count, updated_students)

        teachers = Participant.objects.filter(cohort=cohort, role=Participant.TEACHER)
        actual_teachers = [teacher.user for teacher in teachers]
        self.assertEqual(set(expected_teachers), set(actual_teachers))
        self.assertEqual(len(teachers) - initial_teachers_count, updated_teachers)
