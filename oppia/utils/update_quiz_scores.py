# fix script for updating submitted quiz Scores


def run(): 
    
    from django.db.models import Sum
    from oppia.quiz.models import Quiz, QuizAttempt, QuizAttemptResponse
    
    attempts = QuizAttempt.objects.filter(score=0)
    
    for a in attempts:
        attempt_score = QuizAttemptResponse.objects.filter(quizattempt=a).aggregate(total_score=Sum('score'))
        if a.score != attempt_score['total_score'] and attempt_score['total_score'] is not None:
            print attempt_score
            a.score = attempt_score['total_score']
            a.save()
    
if __name__ == "__main__":
    import django
    django.setup()
    run() 