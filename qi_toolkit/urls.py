from django.conf.urls.defaults import *
import robots
from django.conf import settings


urlpatterns = patterns('',          
    url(r'^robots.txt',     robots.robots_txt,          name='robots_txt'),
)

if "FAVICON_URL" in settings:
    urlpatterns += patterns('',          
	    (r'^favicon\.ico$', 'django.views.generic.simple.redirect_to', {'url': settings.FAVICON_URL}),
    )
