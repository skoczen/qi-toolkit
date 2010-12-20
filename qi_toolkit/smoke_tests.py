from django.test.client import Client
from nose.tools import istest, nottest, assert_true
from django.core.urlresolvers import reverse
from django.db import transaction

DEFAULT_SMOKE_TEST_OPTIONS = {
    'client'            : Client(),
    'reverse_args'      : (),
    'reverse_kwargs'    : {},
    'status_code'       : 200,
    'data'              : {},
    'method'            : "GET",
    'verbose'           : True,
}

class Config(object):
    pass

@nottest 
@transaction.commit_manually
def smoke_test(url_name, *args, **kwargs):
    try:
        config = Config()
        config.__dict__.update(DEFAULT_SMOKE_TEST_OPTIONS)
        config.__dict__.update(**kwargs)

        if config.verbose:
            print "Smoke Test: %s  " % (url_name),

        reverse_url = None
        fail_error = None
        try:
            reverse_url = reverse(url_name, args=config.reverse_args, kwargs=config.reverse_kwargs)
        except:
            pass
        if not reverse_url:
            fail_error = "URL Reversing for '%s' failed." % (url_name)
        assert_true(reverse_url)

        if reverse_url:
            if config.method=="POST":
                response = config.client.post(reverse_url, config.data)
            else:
                response = config.client.get(reverse_url, config.data)
            if config.verbose:
                print "%s" % (response.status_code)

            if not response.status_code == config.status_code:
                fail_error = "Status code fail. Expected %s.  Got %s" %(response.status_code, config.status_code)
            assert_true(response.status_code == config.status_code)
    except:
        assert 1==0, fail_error
        pass
    transaction.rollback()
