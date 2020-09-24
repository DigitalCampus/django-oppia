from oppia.models import Course, Activity, Tracker, Media
from oppia.test import OppiaTestCase


class MainModelsCoreTest(OppiaTestCase):
    fixtures = ['tests/test_user.json',
                'tests/test_oppia.json',
                'tests/test_quiz.json',
                'tests/test_permissions.json',
                'default_gamification_events.json',
                'tests/test_tracker.json',
                'tests/test_gamification.json',
                'tests/test_course_permissions.json']

    def setUp(self):
        super(MainModelsCoreTest, self).setUp()
        self.course = Course.objects.get(pk=1)
        self.reference_course = Course.objects.get(pk=4)

    '''
    COURSE Model
    '''
    # test course.__str__()
    def test_course_get_title(self):
        self.assertEqual('Antenatal Care Part 1', self.course.get_title())

    # test course.no_distinct_downloads()
    def test_course_no_distinct_downloads(self):
        self.assertEqual(4, self.course.no_distinct_downloads())

    # Course.no_downloads
    def test_course_no_downloads(self):
        self.assertEqual(55, self.course.no_downloads())

    def test_course_get_activity_today(self):
        self.assertEqual(0, self.course.get_activity_today())

    def test_course_get_activity_week(self):
        self.assertEqual(0, self.course.get_activity_week())

    def test_course_has_quizzes(self):
        self.assertTrue(self.course.has_quizzes())

    def test_course_has_no_quizzes(self):
        self.assertFalse(self.reference_course.has_quizzes())

    def test_course_has_feedback(self):
        self.assertFalse(self.course.has_feedback())

    # test course is_first_download()
    def test_course_first_download_admin(self):
        Tracker.objects.filter(user=self.admin_user,
                               course=self.course,
                               type='download').delete()
        self.assertTrue(self.course.is_first_download(self.admin_user))

    def test_course_first_download_staff(self):
        Tracker.objects.filter(user=self.staff_user,
                               course=self.course,
                               type='download').delete()
        self.assertTrue(self.course.is_first_download(self.staff_user))

    def test_course_first_download_teacher(self):
        Tracker.objects.filter(user=self.teacher_user,
                               course=self.course,
                               type='download').delete()
        self.assertTrue(self.course.is_first_download(self.teacher_user))

    def test_course_first_download_user(self):
        Tracker.objects.filter(user=self.normal_user,
                               course=self.course,
                               type='download').delete()
        self.assertTrue(self.course.is_first_download(self.normal_user))

    # test course is not first_download()
    def test_course_not_first_download_admin(self):
        self.assertFalse(self.course.is_first_download(self.admin_user))

    def test_course_not_first_download_staff(self):
        self.assertFalse(self.course.is_first_download(self.staff_user))

    def test_course_not_first_download_teacher(self):
        self.assertFalse(self.course.is_first_download(self.teacher_user))

    def test_course_not_first_download_user(self):
        self.assertFalse(self.course.is_first_download(self.normal_user))

    def test_course_sections(self):
        sections = self.course.sections()
        self.assertEqual(13, len(sections))

    def test_reference_course_sections(self):
        sections = self.reference_course.sections()
        self.assertEqual(1, len(sections))

    def test_pre_test_score_course(self):
        score = Course.get_pre_test_score(self.course, self.normal_user)
        self.assertEqual(None, score)

    def test_pre_test_score_reference(self):
        score = Course.get_pre_test_score(self.reference_course,
                                          self.normal_user)
        self.assertRaises(Activity.DoesNotExist)
        self.assertEqual(None, score)

    '''
    ACTIVITY model
    '''
    # Activity has next
    def test_activity_next_activity_within_section(self):
        activity = Activity.objects.get(pk=3)
        self.assertEqual('fe67f01e97820f2b5b003bf9bfd9f45a12139',
                         activity.get_next_activity().digest)

    def test_activity_next_activity_outside_section(self):
        activity = Activity.objects.get(pk=18)
        self.assertEqual('f9f0e86f5c5f18a719da21d62a3a9b0c12154',
                         activity.get_next_activity().digest)

    def test_activity_next_activity_end_of_course(self):
        activity = Activity.objects.get(pk=222)
        self.assertEqual(None, activity.get_next_activity())

    # Activity has previous
    def test_activity_previous_activity_within_section(self):
        activity = Activity.objects.get(pk=3)
        self.assertEqual('11cc12291f730160c324b727dd2268b612137',
                         activity.get_previous_activity().digest)

    def test_activity_previous_activity_outside_section(self):
        activity = Activity.objects.get(pk=19)
        self.assertEqual('d95762029b6285dae57385341145c40112153cr0s2a1p80a0',
                         activity.get_previous_activity().digest)

    def test_activity_previous_activity_beginning_of_course(self):
        activity = Activity.objects.get(pk=1)
        self.assertEqual(None, activity.get_previous_activity())

    def test_activity_event_points_quiz(self):
        activity = Activity.objects.get(pk=1)
        event_points = activity.get_event_points()
        self.assertEqual(4, len(event_points['events']))
        self.assertEqual("Inherited from global defaults",
                         event_points['source'])

    def test_activity_event_points_page(self):
        activity = Activity.objects.get(pk=2)
        event_points = activity.get_event_points()
        self.assertEqual(1, len(event_points['events']))
        self.assertEqual("Inherited from course", event_points['source'])

    def test_activity_event_points_custom(self):
        activity = Activity.objects.get(pk=373)
        event_points = activity.get_event_points()
        self.assertEqual(1, len(event_points['events']))
        self.assertEqual("Custom Points", event_points['source'])
        self.assertEqual(123, event_points['events'][0].points)

    '''
    MEDIA Model
    '''
    def test_media_get_event_points_default(self):
        media = Media.objects.get(pk=1)
        self.assertEqual(4, len(media.get_event_points()['events']))
        media_started_event = media.get_event_points()['events'][0]
        self.assertEqual(20, media_started_event.points)

    def test_media_get_event_points_custom(self):
        media = Media.objects.get(pk=4)
        self.assertEqual(4, len(media.get_event_points()['events']))
        media_started_event = media.get_event_points()['events'][0]
        self.assertEqual(100, media_started_event.points)
