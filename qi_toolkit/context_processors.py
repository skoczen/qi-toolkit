from django.conf import settings

def add_env_to_request(request):
    "Adds the ENV context to the template"
    try:
        return {'ENV' : settings.ENV }
    except:
        return {}

def add_favicon_to_request(request):
    "Adds the FAVICON_URL context to the template"
    try:
        return {'FAVICON_URL' : settings.FAVICON_URL }
    except:
        return {}    