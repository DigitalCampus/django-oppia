
OPPIA_DEFAULT_POINTS = {
        'REGISTER': 100,  # given when user first registers
        'QUIZ_FIRST_ATTEMPT': 20,  # for the first attempt at a quiz
        'QUIZ_ATTEMPT': 10,  # for any subsequent attempts at a quiz
        'QUIZ_FIRST_ATTEMPT_THRESHOLD': 100,  # Threshold for getting bonus points for first attempt at quiz (must be 0-100)
        'QUIZ_FIRST_ATTEMPT_BONUS': 50,  # Bonus points for getting over the threshold on first attempt at quiz
        'ACTIVITY_COMPLETED': 10,  # for completing an activity
        'MEDIA_STARTED': 20,  # for starting media
        'MEDIA_PLAYING_INTERVAL': 30,  # interval in seconds for which points are given
        'MEDIA_PLAYING_POINTS_PER_INTERVAL': 5,  # no points per interval media is playing
        'MEDIA_MAX_POINTS': 200,  # the maximum number of points available for any single media play
        'COURSE_DOWNLOADED': 50,  # for downloading a course

    # TODO  - these values are deprecated and will be removed in v0.11.0
        'QUIZ_ATTEMPT_OWNER': 5,  # given to the quiz owner when another user attempts their quiz
        'QUIZ_CREATED': 200,  # for creating a quiz
    }
