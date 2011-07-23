import sys

class classproperty(property):
    def __get__(self, cls, owner):
        return self.fget.__get__(None, owner)()


def render_to(template):
    from django.shortcuts import render_to_response
    from django.template import RequestContext
    
    """
    Decorator for Django views that sends returned dict to render_to_response function
    with given template and RequestContext as context instance.

    If view doesn't return dict then decorator simply returns output.
    Additionally view can return two-tuple, which must contain dict as first
    element and string with template name as second. This string will
    override template name, given as parameter

    Parameters:

     - template: template name to use
    """
    def renderer(func):
        def wrapper(request, *args, **kw):
            output = func(request, *args, **kw)
            if isinstance(output, (list, tuple)):
                return render_to_response(output[1], output[0], RequestContext(request))
            elif isinstance(output, dict):
                return render_to_response(template, output, RequestContext(request))
            return output
        return wrapper
    return renderer

def exception_string():
    import traceback
    import sys
    return '\n'.join(traceback.format_exception(*sys.exc_info()))
    
def print_exception():
    print "######################## Exception #############################"
    print exception_string()
    print "################################################################"


def json_view(func):
    from django.http import HttpResponse
    from django.utils import simplejson
    from django.core.mail import mail_admins
    from django.utils.translation import ugettext as _
    import sys
    
    def wrap(request, *a, **kw):
        response = None
        try:
            response = dict(func(request, *a, **kw))
            if 'result' not in response:
                response['result'] = 'ok'
        except KeyboardInterrupt:
            # Allow keyboard interrupts through for debugging.
            raise
        except Exception, e:
            # Mail the admins with the error
            exc_info = sys.exc_info()
            subject = 'JSON view error: %s' % request.path
            try:
                request_repr = repr(request)
            except:
                request_repr = 'Request repr() unavailable'
            import traceback
            message = 'Traceback:\n%s\n\nRequest:\n%s' % (
                '\n'.join(traceback.format_exception(*exc_info)),
                request_repr,
                )
            mail_admins(subject, message, fail_silently=True)

            # Come what may, we're returning JSON.
            if hasattr(e, 'message'):
                msg = e.message
            else:
                msg = _('Internal error')+': '+str(e)
            response = {'result': 'error',
                        'text': msg}

        json = simplejson.dumps(response)
        return HttpResponse(json, mimetype='application/json')
    return wrap

def silence_print():
    old_printerators=[sys.stdout,sys.stderr,sys.stdin,sys.__stdout__,sys.__stderr__,sys.__stdin__][:]
    sys.stdout,sys.stderr,sys.stdin,sys.__stdout__,sys.__stderr__,sys.__stdin__=dummyStream(),dummyStream(),dummyStream(),dummyStream(),dummyStream(),dummyStream()
    return old_printerators

def unsilence_print(printerators):
    sys.stdout,sys.stderr,sys.stdin,sys.__stdout__,sys.__stderr__,sys.__stdin__=printerators


class dummyStream:
    ''' dummyStream behaves like a stream but does nothing. '''
    # via http://www.answermysearches.com/python-temporarily-disable-printing-to-console/232/
    def __init__(self): pass
    def write(self,data): pass
    def read(self,data): pass
    def flush(self): pass
    def close(self): pass

def noprint(func):
    def wrapper(*args, **kw):
        _p = silence_print()
        output = func(*args, **kw)
        unsilence_print(_p)
        return output
    return wrapper
