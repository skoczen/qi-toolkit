from django.conf import settings

def add_env_to_request(self, request):
    "Adds the ENV context to the template"
    try:
        return {'ENV' : settings.ENV }
    except:
        return {}