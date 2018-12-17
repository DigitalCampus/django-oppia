"""OppiaMobile URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""

from django.conf import settings
from django.conf.urls import url, include
from django.contrib import admin

urlpatterns = [
    url(r'^', include('oppia.urls')),
    url(r'^api/', include('api.urls')),
    url(r'^content/', include('content.urls')),
    url(r'^profile/', include('profile.urls')),
    url(r'^reports/', include('reports.urls')),
    url(r'^activitylog/', include('activitylog.urls')),
    url(r'^viz/', include('viz.urls')),
    url(r'^av/', include('av.urls')),
    url(r'^gamification/', include('gamification.urls')),
    url(r'^admin/', admin.site.urls),
]

if settings.DEVICE_ADMIN_ENABLED:
    gcmpatterns = [ url(r'^deviceadmin/', include('deviceadmin.urls')), ]
    urlpatterns += gcmpatterns
