
from django.conf.urls import include
from django.urls import path
from django.utils.translation import gettext_lazy as _
from django.contrib import admin

admin.site.index_title = _(u'Welcome to the OppiaMobile admin pages')

urlpatterns = [
    path('', include('oppia.urls', namespace='oppia')),
    path('api/', include('api.urls')),
    path('profile/', include('profile.urls', namespace='profile')),
    path('reports/', include('reports.urls')),
    path('activitylog/', include('activitylog.urls')),
    path('av/', include('av.urls', namespace="oppia_av")),
    path('gamification/', include('gamification.urls')),
    path('admin/', admin.site.urls),
    path('integrations/', include('integrations.urls')),
    path('quiz/', include('quiz.urls')),
    path('serverregistration/', include('serverregistration.urls')),
    path('accounts/', include('django.contrib.auth.urls')),
]
