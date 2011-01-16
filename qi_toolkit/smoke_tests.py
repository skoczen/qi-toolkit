from django.test.client import Client
from nose.tools import istest, nottest, assert_true
from django.core.urlresolvers import reverse
from django.db import transaction
import re

title_re = re.compile("<title>.*?<\/title>",re.I)

DEFAULT_SMOKE_TEST_OPTIONS = {
    'client'            : Client(),
    'reverse_args'      : (),
    'reverse_kwargs'    : {},
    'status_code'       : 200,
    'data'              : {},
    'method'            : "GET",
    'verbose'           : True,
    'check_title'       : False,
}

class Config(object):
    pass

@nottest
@transaction.commit_manually
def smoke_test(url_name, *args, **kwargs):
    __test__ = True
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
        
        if config.check_title:
            fail_error = "Page is missing a title. %s" % (reverse_url)
            assert title_re.search(response.content) != None
        
        transaction.rollback()

    except:
        print fail_error
        from qi_toolkit.helpers import print_exception
        print_exception()
        transaction.rollback()
        assert 1==0

