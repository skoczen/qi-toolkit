from django.conf import settings

class EnvMiddleware(object):
    
def process_request(self, request):
    try:
        request['context']['ENV'] = settings.ENV
    except:
        pass
    return request