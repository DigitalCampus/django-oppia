
# oppia/local_settings.py

def modify(settings):

    settings['INSTALLED_APPS'] += ('oppia.quiz',
                                   'oppia.viz',
                                   'oppia.preview',
                                   'oppia.av',
                                   'oppia.profile',
                                   'oppia.reports',
                                   'oppia.settings',
                                   'oppia.summary',
                                   'oppia.activitylog',
                                   'oppia.gamification',
                                   'crispy_forms',
                                   'tastypie',
                                   'sorl.thumbnail', )
    settings['MIDDLEWARE_CLASSES'] += ('oppia.middleware.LoginRequiredMiddleware', )

    settings['TEMPLATES'][0]['OPTIONS']['context_processors'] += [
            'oppia.context_processors.get_points',
            'oppia.context_processors.get_version',
            'oppia.context_processors.get_settings', ]

    settings['LOGIN_EXEMPT_URLS'] = (
         r'^server/$',
         r'^profile/login/$',
         r'^profile/register/',
         r'^profile/reset/',
         r'^profile/setlang/$',
         r'^profile/delete/complete/$',
         
         r'^mobile/scorecard/$',  # - auth handled by api_key
         r'^$',
         r'^about/$',
         r'^terms/$',
         r'^api/',  # allow any URL under api/* - auth handled by api_key
         r'^modules/api/',  # allow any URL under modules/api/* - auth handled by api_key
         r'^badges/api/',  # allow any URL under badges/api/* - auth handled by api_key

         r'^content/video-embed-helper/$',
         r'^media/temp/',
         r'^media/uploaded/',
    )

    settings['CRISPY_TEMPLATE_PACK'] = 'bootstrap3'

    settings['OPPIA_METADATA'] = {
        'NETWORK': True,  # 'DEVICE_ID': True,
        'SIM_SERIAL': True,
        'WIFI_ON': True,
        'NETWORK_CONNECTED': True,
        'BATTERY_LEVEL': True,
        'GPS': False,
    }

    settings['OPPIA_ALLOW_SELF_REGISTRATION'] = True    # turns on/off ability for users to self register

    settings['OPPIA_SHOW_GRAVATARS'] = True

    settings['OPPIA_STAFF_ONLY_UPLOAD'] = True          # prevents anyone without is_staff status being able to upload courses,
    # setting to False allows any registered user to upload a course

    settings['OPPIA_POINTS_ENABLED'] = True            # determines if the points system is enabled
    # if OPPIA POINTS_ENABLED is false, then the next 3 settings are ignored
    settings['OPPIA_STAFF_EARN_POINTS'] = False         # prevent staff from earning points
    settings['OPPIA_COURSE_OWNERS_EARN_POINTS'] = False  # stops owners of courses earning points
    settings['OPPIA_TEACHERS_EARN_POINTS'] = False      # stops teachers of courses earning points

    settings['OPPIA_BADGES_ENABLED'] = True            # determines if the badges system is enabled

    settings['BADGE_AWARD_METHOD_ALL_ACTIVITIES'] = 'all activities'
    settings['BADGE_AWARD_METHOD_FINAL_QUIZ'] = 'final quiz'
    settings['BADGE_AWARD_METHOD_ALL_QUIZZES'] = 'all quizzes'

    settings['BADGE_AWARDING_METHOD'] = settings['BADGE_AWARD_METHOD_ALL_ACTIVITIES']

    settings['OPPIA_GOOGLE_ANALYTICS_ENABLED'] = True
    settings['OPPIA_GOOGLE_ANALYTICS_CODE'] = 'UA-3609005-11'
    settings['OPPIA_GOOGLE_ANALYTICS_DOMAIN'] = 'oppia-mobile.org'

    settings['OPPIA_MAX_UPLOAD_SIZE'] = 5242880         # max course file upload size - in bytes

    settings['OPPIA_VIDEO_FILE_TYPES'] = ("video/m4v", "video/mp4", "video/3gp", "video/3gpp")
    settings['OPPIA_AUDIO_FILE_TYPES'] = ("audio/mpeg", "audio/amr", "audio/mp3")
    settings['OPPIA_MEDIA_FILE_TYPES'] = settings['OPPIA_VIDEO_FILE_TYPES'] + settings['OPPIA_AUDIO_FILE_TYPES']

    settings['OPPIA_MEDIA_IMAGE_FILE_TYPES'] = ("image/png", "image/jpeg")

    settings['OPPIA_UPLOAD_TRACKER_FILE_TYPES'] = [("application/json")]

    settings['OPPIA_EXPORT_LOCAL_MINVERSION'] = 2017011400  # min version of the export block to process the quizzes locally

    settings['API_LIMIT_PER_PAGE'] = 0

    settings['DEVICE_ADMIN_ENABLED'] = False

    if settings['DEVICE_ADMIN_ENABLED']:
        settings['INSTALLED_APPS'] += ('oppia.deviceadmin', 'gcm', )
        settings['GCM_APIKEY'] = 'OPPIA_GOOGLEAPIKEY'
        settings['GCM_DEVICE_MODEL'] = 'oppia.deviceadmin.models.UserDevice'

    settings['DEVELOPMENT_SERVER'] = True
