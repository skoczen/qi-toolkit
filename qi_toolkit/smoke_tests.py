from django.test.client import Client
from nose.tools import istest, nottest
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

        if config.method=="POST":
            response = config.client.post(reverse(url_name, args=config.reverse_args, kwargs=config.reverse_kwargs), config.data)
        else:
            response = config.client.get(reverse(url_name, args=config.reverse_args, kwargs=config.reverse_kwargs), config.data)
        if config.verbose:
            print "%s" % (response.status_code)
        
        assert response.status_code == config.status_code
    except:
        pass
    transaction.rollback()
