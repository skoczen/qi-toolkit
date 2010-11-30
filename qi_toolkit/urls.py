from django.conf.urls.defaults import *
import robots


urlpatterns += patterns('',          
    url(r'^robots.txt',     robots.robots_txt,          name='robots_txt'),
)