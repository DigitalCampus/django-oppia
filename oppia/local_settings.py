# oppia/local_settings.py

def modify(settings):
    
    settings['MIDDLEWARE_CLASSES'] += ('oppia.middleware.LoginRequiredMiddleware',)
    settings['TEMPLATE_CONTEXT_PROCESSORS'] += ('oppia.context_processors.get_points',)
    settings['TEMPLATE_CONTEXT_PROCESSORS'] += ('oppia.context_processors.get_version',)
    settings['LOGIN_EXEMPT_URLS'] = (
         r'^profile/login/$',
         r'^profile/register/',
         r'^profile/reset/',
         r'^profile/setlang/$',
         r'^mobile/scorecard/$',# - auth handled by api_key
         r'^$',
         r'^about/$',
         r'^terms/$',
         r'^api/', # allow any URL under api/* - auth handled by api_key
         r'^modules/api/', # allow any URL under modules/api/* - auth handled by api_key
         r'^badges/api/', # allow any URL under badges/api/* - auth handled by api_key
    ) 
    
    
    settings['OPPIA_POINTS'] = {
        'REGISTER':100, # given when user first registers
        'QUIZ_ATTEMPT_OWNER':5, # given to the quiz owner when another user attempts their quiz 
        'QUIZ_FIRST_ATTEMPT':20, # for the first attempt at a quiz 
        'QUIZ_ATTEMPT':10, # for any subsequent attempts at a quiz 
        'QUIZ_FIRST_ATTEMPT_THRESHOLD':100, # Threshold for getting bonus points for first attempt at quiz (must be 0-100)
        'QUIZ_FIRST_ATTEMPT_BONUS':50, # Bonus points for getting over the threshold on first attempt at quiz 
        'QUIZ_CREATED':200, # for creating a quiz
        'ACTIVITY_COMPLETED':10, # for completing an activity
        'MEDIA_PLAYED':20, # for playing media
        'COURSE_DOWNLOADED':50, # for downloading a course
        }
       
    settings['MAX_UPLOAD_SIZE'] = 5242880 # max course file upload size - in bytes          
                                
    
    