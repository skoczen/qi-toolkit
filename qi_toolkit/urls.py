from django.conf.urls.defaults import *
import robots


url = parser.url
urlpatterns = parser.patterns('',                      
    url(r'^robots.txt',     robots.robots_txt,          name='robots_txt'),

)