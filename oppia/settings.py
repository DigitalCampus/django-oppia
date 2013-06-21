# oppia.settings.py

def modify(settings):
    
    settings['MIDDLEWARE_CLASSES'] += ('oppia.middleware.LoginRequiredMiddleware',)
    settings['TEMPLATE_CONTEXT_PROCESSORS'] += ('oppia.context_processors.get_points',)
    settings['LOGIN_EXEMPT_URLS'] = (
         r'^profile/login/$',
         r'^profile/register/',
         r'^profile/reset/',
         r'^profile/setlang/$',
         r'^$',
         r'^about/$',
         r'^terms/$',
         r'^api/', # allow any URL under api/*
         r'^modules/api/', # allow any URL under modules/api/*
    ) 
    
    