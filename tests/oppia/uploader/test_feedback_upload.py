import os

from django.conf import settings
from quiz.models import QuizProps, QuestionProps, QuizAttempt

from tests.oppia.uploader.quiz_upload_testcase import QuizUploadTestCase


class QuizUploadTest(QuizUploadTestCase):
    fixtures = ['tests/test_user.json',
                'tests/test_oppia.json',
                'tests/test_permissions.json',
                'default_badges.json',
                'tests/test_course_permissions.json']

    original_feedback_json_file = os.path.join(settings.TEST_RESOURCES, 'quizzes/feedback_1.json')
    updated_feedback_json_file = os.path.join(settings.TEST_RESOURCES, 'quizzes/feedback_1_edited.json')
    feedback_attempt_1_json_file = os.path.join(settings.TEST_RESOURCES, 'quizzes/feedback_attempt_1.json')
    feedback_attempt_2_json_file = os.path.join(settings.TEST_RESOURCES, 'quizzes/feedback_attempt_2.json')

    def upload_feedback(self, feedback_json_file):
        return self.upload(feedback_json_file, 'feedback')

    def test_upload_feedback_from_json(self):
        # 1. Upload feedback activity
        feedback_obj, feedback_json = self.upload_feedback(self.original_feedback_json_file)
        # 2. Assert title is correct
        self.assertEqual('{"en": "Feedback with optional"}', feedback_obj.title)

        # 3. Assert feedback props values
        self.assert_quiz_props(feedback_obj, feedback_json)

        # 4. Assert feedback questions
        questions_json = feedback_json['questions']
        self.assertEqual(3, feedback_obj.questions.count())
        for index, question in enumerate(feedback_obj.questions.all()):
            question_json = questions_json[index]['question']
            # 5. Assert question props
            self.assert_question_props(question, question_json)

    def test_upload_edited_feedback_from_json(self):
        # Upload edited feedback that was exported preserving the IDs
        original_feedback_obj, original_feedback_json = self.upload_feedback(self.original_feedback_json_file)
        original_feedback_id = original_feedback_obj.id
        original_feedback_props = QuizProps.objects.filter(quiz=original_feedback_obj)
        original_question = original_feedback_obj.questions.first()
        original_question_props = QuestionProps.objects.filter(question=original_question)

        original_feedback_digest = original_feedback_props.get(name="digest").value
        original_moodle_quiz_id = original_feedback_props.get(name="moodle_quiz_id").value
        original_moodle_question_id = original_question_props.get(name="moodle_question_id").value

        self.assertEqual('{"en": "Feedback with optional"}', original_feedback_obj.title)
        self.assertEqual('{"en": "This multiple choice is required. Do it."}', original_question.title)
        self.assert_quiz_props(original_feedback_obj, original_feedback_json)

        updated_feedback_obj, updated_feedback_json = self.upload_feedback(self.updated_feedback_json_file)
        updated_feedback_id = updated_feedback_obj.id
        updated_quiz_props = QuizProps.objects.filter(quiz=updated_feedback_obj)
        updated_question = updated_feedback_obj.questions.first()
        updated_question_props = QuestionProps.objects.filter(question=updated_question)

        self.assertEqual('{"en": "Feedback with optional updated"}', updated_feedback_obj.title)
        self.assertEqual('{"en": "(Updated) This multiple choice is required. Do it."}', updated_question.title)
        self.assert_quiz_props(updated_feedback_obj, updated_feedback_json)

        updated_feedback_digest = updated_quiz_props.get(name="digest").value
        updated_moodle_quiz_id = updated_quiz_props.get(name="moodle_quiz_id").value
        updated_moodle_question_id = updated_question_props.get(name="moodle_question_id").value

        self.assertEqual(original_feedback_id, updated_feedback_id)
        self.assertEqual(original_feedback_digest, updated_feedback_digest)
        self.assertEqual(original_moodle_quiz_id, updated_moodle_quiz_id)
        self.assertEqual(original_moodle_question_id, updated_moodle_question_id)

    def test_quiz_attempts_when_feedback_is_reuploaded(self):
        # 1. Upload feedback activity
        original_feedback_obj, original_feedback_json = self.upload_feedback(self.original_feedback_json_file)

        # 2. Assert no quiz attempts yet
        self.assertEqual(0, QuizAttempt.objects.filter(quiz=original_feedback_obj).count())

        # 3. Send quiz attempt 1
        self.send_quiz_attempt(self.feedback_attempt_1_json_file)

        # 4. Assert there is one quiz attempt
        self.assertEqual(1, QuizAttempt.objects.filter(quiz=original_feedback_obj).count())

        # 5. Re-upload the feedback activity (edited) that was exported preserving the IDs
        updated_quiz_obj, updated_quiz_json = self.upload_feedback(self.updated_feedback_json_file)

        # 6. Assert there is one quiz attempt for the edited quiz
        self.assertEqual(1, QuizAttempt.objects.filter(quiz=updated_quiz_obj).count())

        # 7. Send quiz attempt 2
        self.send_quiz_attempt(self.feedback_attempt_2_json_file)

        # 8. Assert there are now 2 quiz attempts for the edited quiz
        self.assertEqual(2, QuizAttempt.objects.filter(quiz=updated_quiz_obj).count())

