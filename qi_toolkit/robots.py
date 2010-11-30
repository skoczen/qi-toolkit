from django.http import HttpResponse
from django.conf import settings

def robots_txt(request):
    try:
        if settings.ENV == "STAGING" or settings.ENV == "DEV":
            return HttpResponse("User-agent: *\nDisallow: /", mimetype="text/plain")
    except:
        pass

    return HttpResponse("User-agent: *\nDisallow: ", mimetype="text/plain")
