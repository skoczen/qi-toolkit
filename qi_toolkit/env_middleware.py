from django.conf import settings

class EnvMiddleware(object):
    "Adds the ENV context to the template"

    def process_request(self, request):
        try:
            request['context']['ENV'] = settings.ENV
        except:
            pass
        return request