# coding: utf-8

"""
Management command to update manually scored short answer questions
"""
import csv

from django.core.management.base import BaseCommand
from django.db.models import Sum

from oppia.models import Tracker
from quiz.models import QuizAttemptResponse, QuizProps

INPUT_FORMAT = {
                  'question': 0,
                  'qar_id': 1,
                  'response': 2,
                  'score': 3,
                  'revised_score': 4,
              }


class Command(BaseCommand):
    help = "Updates the scores for short answer questions"

    def add_arguments(self, parser):
        parser.add_argument('file')

    def handle(self, *args, **options):

        # load CSV file
        with open(options['file'], 'rb') as csvfile:
            file_reader = csv.reader(csvfile, delimiter=',', quotechar='"')

            # log max qar_id
            max_qar_id = 0
            # loop through each row and determine if the score is different
            for counter, row in enumerate(file_reader):

                # if empty row then skip and continue
                if row[INPUT_FORMAT['qar_id']] == 'QARID' or row[INPUT_FORMAT['qar_id']] == '' or row[INPUT_FORMAT['qar_id']] is None:
                    continue

                qar = QuizAttemptResponse.objects.get(pk=long(row[INPUT_FORMAT['qar_id']]))

                if qar.id > max_qar_id:
                    max_qar_id = qar.id

                if row[INPUT_FORMAT['revised_score']] == '' or row[INPUT_FORMAT['revised_score']] is None or row[INPUT_FORMAT['revised_score']] == row[INPUT_FORMAT['score']]:
                    continue

                try:
                    if int(row[INPUT_FORMAT['revised_score']]) == int(qar.score):
                        continue
                except ValueError:
                    continue

                qar.score = row[INPUT_FORMAT['revised_score']]
                qar.save()

                quiz_attempt = qar.quizattempt

                # update the quiz attempt total score
                new_quiz_score = QuizAttemptResponse.objects.filter(quizattempt=qar.quizattempt).aggregate(new_score=Sum('score'))
                quiz_attempt.score = new_quiz_score['new_score']
                quiz_attempt.save()

                quiz_score_percent = quiz_attempt.score * 100 / quiz_attempt.maxscore

                # check if they have now reached the pass mark for the quiz and update the tracker activity
                quiz_threshold = QuizProps.objects.get(name='passthreshold', quiz=quiz_attempt.quiz)

                if quiz_score_percent >= quiz_threshold:
                    print(quiz_score_percent + ":" + quiz_threshold)
                    try:
                        tracker = Tracker.objects.get(user=quiz_attempt.user, uuid=quiz_attempt.instance_id)
                        tracker.completed = True
                        tracker.save()
                        print("tracker updated")
                    except Tracker.DoesNotExist:
                        pass

            print("Max QAR id - " + str(max_qar_id))
