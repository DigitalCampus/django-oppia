
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
         r'^contact/$',
         r'^api/', # allow any URL under api/*
         r'^quiz/api/', # allow any URL under quiz/api/*
    ) 
    
    