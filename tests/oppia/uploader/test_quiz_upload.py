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
    original_quiz_json_file = os.path.join(settings.TEST_RESOURCES, 'quizzes/quiz_1.json')
    updated_quiz_json_file = os.path.join(settings.TEST_RESOURCES, 'quizzes/quiz_1_edited.json')
    quiz_attempt_1_json_file = os.path.join(settings.TEST_RESOURCES, 'quizzes/quiz_attempt_1.json')
    quiz_attempt_2_json_file = os.path.join(settings.TEST_RESOURCES, 'quizzes/quiz_attempt_2.json')

    def upload_quiz(self, quiz_json_file):
        return self.upload(quiz_json_file, 'quiz')

    def test_upload_quiz_from_json(self):
        # 1. Upload quiz
        quiz_obj, quiz_json = self.upload_quiz(self.original_quiz_json_file)
        
        # 2. Assert title is correct
        self.assertEqual('{"en": "Test Quiz"}', quiz_obj.title)

        # 3. Assert quiz props values
        self.assert_quiz_props(quiz_obj, quiz_json)

        # 4. Assert quiz questions
        questions_json = quiz_json['questions']
        self.assertEqual(3, quiz_obj.questions.count())
        for index, question in enumerate(quiz_obj.questions.all()):
            question_json = questions_json[index]['question']
            # 5. Assert question props
            self.assert_question_props(question, question_json)

    def test_upload_edited_quiz_from_json(self):
        original_quiz_obj, original_quiz_json = self.upload_quiz(self.original_quiz_json_file)
        original_quiz_id = original_quiz_obj.id
        original_quiz_props = QuizProps.objects.filter(quiz=original_quiz_obj)
        original_question = original_quiz_obj.questions.first()
        original_question_props = QuestionProps.objects.filter(question=original_question)

        original_quiz_digest = original_quiz_props.get(name="digest").value
        original_moodle_quiz_id = original_quiz_props.get(name="moodle_quiz_id").value
        original_moodle_question_id = original_question_props.get(name="moodle_question_id").value
        original_moodle_question_bank_id = original_question_props.get(name="moodle_question_latest_version_id").value

        self.assertEqual('{"en": "Test Quiz"}', original_quiz_obj.title)
        self.assertEqual('{"en": "Test Question"}',  original_question.title)
        self.assert_quiz_props(original_quiz_obj, original_quiz_json)

        updated_quiz_obj, updated_quiz_json = self.upload_quiz(self.updated_quiz_json_file)
        updated_quiz_id = updated_quiz_obj.id
        updated_quiz_props = QuizProps.objects.filter(quiz=updated_quiz_obj)
        updated_question = updated_quiz_obj.questions.first()
        updated_question_props = QuestionProps.objects.filter(question=updated_question)

        self.assertEqual('{"en": "Test Quiz Updated"}', updated_quiz_obj.title)
        self.assertEqual('{"en": "Test Question Updated"}',  updated_question.title)
        self.assert_quiz_props(updated_quiz_obj, updated_quiz_json)

        updated_quiz_digest = updated_quiz_props.get(name="digest").value
        updated_moodle_quiz_id = updated_quiz_props.get(name="moodle_quiz_id").value
        updated_moodle_question_id = updated_question_props.get(name="moodle_question_id").value
        updated_moodle_question_bank_id = updated_question_props.get(name="moodle_question_latest_version_id").value

        self.assertEqual(original_quiz_id, updated_quiz_id)
        self.assertEqual(original_quiz_digest, updated_quiz_digest)
        self.assertEqual(original_moodle_quiz_id, updated_moodle_quiz_id)
        self.assertEqual(original_moodle_question_id, updated_moodle_question_id)
        self.assertNotEqual(original_moodle_question_bank_id, updated_moodle_question_bank_id)

    def test_quiz_attempts_when_quiz_is_reuploaded(self):
        # 1. Upload quiz
        original_quiz_obj, original_quiz_json = self.upload_quiz(self.original_quiz_json_file)

        # 2. Assert no quiz attempts yet
        self.assertEqual(0, QuizAttempt.objects.filter(quiz=original_quiz_obj).count())

        # 3. Send quiz attempt 1
        self.send_quiz_attempt(self.quiz_attempt_1_json_file)

        # 4. Assert there is one quiz attempt
        self.assertEqual(1, QuizAttempt.objects.filter(quiz=original_quiz_obj).count())

        # 5. Re-upload the quiz (edited)
        updated_quiz_obj, updated_quiz_json = self.upload_quiz(self.updated_quiz_json_file)

        # 6. Assert there is one quiz attempt for the edited quiz
        self.assertEqual(1, QuizAttempt.objects.filter(quiz=updated_quiz_obj).count())

        # 7. Send quiz attempt 2
        self.send_quiz_attempt(self.quiz_attempt_2_json_file)

        # 8. Assert there are now 2 quiz attempts for the edited quiz
        self.assertEqual(2, QuizAttempt.objects.filter(quiz=updated_quiz_obj).count())
