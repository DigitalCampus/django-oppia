import xml.etree.ElementTree as ET
import json

from django.core.management.base import BaseCommand
from django.utils.translation import gettext as _

from oppia.models import Activity
from quiz.models import Quiz, QuizProps, Question, QuestionProps


class Command(BaseCommand):
    help = _(u'Backfills the Moodle ids for quizzes')

    def add_arguments(self, parser):

        # required argument to the module.xml file
        parser.add_argument(
            'coursexml',
            type=str,
            help=_(u'Directory and file path to the module.xml file'),
        )

    def handle(self, *args, **options):
        # read file to xml
        doc = ET.parse(options['coursexml'])

        # iterate through the quizzes
        for structure in doc.findall('structure'):
            for section in structure.findall('section'):
                for activities in section.findall('activities'):
                    for activity in activities.findall('activity'):
                        if activity.get("type") == Activity.QUIZ:
                            quiz_content = activity.find('content').text
                            self.process_quiz(quiz_content)

    def process_quiz(self, quiz_content):

        quiz_json = json.loads(quiz_content)

        # find Oppia quiz id - based on digest
        quiz_digest = quiz_json['props']['digest']

        try:
            oppia_quiz = Quiz.objects.get(quizprops__name=QuizProps.DIGEST,
                                          quizprops__value=quiz_digest)
        except Quiz.DoesNotExist:
            self.stdout.write(_(u"Quiz not found"))
            return

        try:
            moodle_quiz_id = quiz_json['props'][QuizProps.MOODLE_QUIZ_ID]
        except KeyError:
            self.stdout.write(_(u"Missing moodle_quiz_id for this quiz"))
            return

        # add/update moodle_quiz_id, moodle_quiz_title and add/update
        # moodle_quiz_desc
        qp_id, created_id = QuizProps.objects.get_or_create(
            quiz=oppia_quiz, name=QuizProps.MOODLE_QUIZ_ID)
        qp_id.value = moodle_quiz_id
        qp_id.save()

        self.stdout.write(_(u"Updated quiz props for %s" % oppia_quiz.title))

        # process the questions
        for question_json in quiz_json['questions']:
            self.process_question(oppia_quiz, question_json)

    def process_question(self, oppia_quiz, question_json):

        # find the question
        question_title = json.dumps(question_json['question']['title'])
        try:
            oppia_question = Question.objects.get(
                quizquestion__quiz=oppia_quiz,
                title=question_title)
        except Question.DoesNotExist:
            self.stdout.write(_(u'Question not found %s' % question_title))
            return

        try:
            moodle_question_id = \
                question_json['question']['props'][QuestionProps.MOODLE_QUESTION_ID]
        except KeyError:
            self.stdout.write(_(u"Missing Moodle data for this question - %s" %
                                question_title))
            return

        # add/update moodle_question_id
        qp_id, created_desc = QuestionProps.objects.get_or_create(
            question=oppia_question, name=QuestionProps.MOODLE_QUESTION_ID)
        qp_id.value = moodle_question_id
        qp_id.save()
        self.stdout.write(_(u"Updated question props for %s" %
                            oppia_question.title))
