from django.http import HttpResponse
from django.conf import settings

def robots_txt(request, allow=False):
    try:
        if settings.ENV == "STAGING" or settings.ENV == "DEV":
            return HttpResponse("User-agent: *\nDisallow: /", mimetype="text/plain")
    except:
        pass
    if allow:
        return HttpResponse("User-agent: *\nAllow: /", mimetype="text/plain")
    else:
        return HttpResponse("User-agent: *\nDisallow: /", mimetype="text/plain")
