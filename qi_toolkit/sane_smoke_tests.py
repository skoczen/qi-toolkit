from djangosanetesting.cases import DatabaseTestCase
from django.test.client import Client
from nose.tools import istest, nottest, assert_true
from django.core.urlresolvers import reverse
import re

title_re = re.compile("<title>.+?<\/title>",re.I)

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


class SmokeTestSuite(DatabaseTestCase):
    def __init__(self, fixtures=[], *args, **kwargs):
        self.fixtures = fixtures
        self.test_configs = []
        super(SmokeTestSuite,self).__init__(*args, **kwargs)

    @nottest
    def add_test(self, url, *args, **kwargs):
        config = Config()
        config.__dict__.update(DEFAULT_SMOKE_TEST_OPTIONS)
        config.__dict__.update(**kwargs)
        config.url_name = url
        self.test_configs.append(config)

    @nottest
    def run_test(self, config):
        fail_error = None
        try:
            fail_error = None
            try:
                reverse_url = reverse(config.url_name, args=config.reverse_args, kwargs=config.reverse_kwargs)
            except:
                fail_error = "URL Reversing for '%s' failed." % (config.url_name)
            
            
            if not fail_error:
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
        except:
            from qi_toolkit.helpers import exception_string
            exception_string()
            fail_error = "Unhandled Fail: \n%s" % (exception_string())
            
        return fail_error

    @nottest
    def run_suite(self):
        success = True
        exceptions = []
        for c in self.test_configs:
            test_results = self.run_test(c)
            if test_results != None:
                exceptions.append({'config':c,'results':test_results})
                success = False
        if not success:
            # I apologize greatly for this line. It was really late. I'll refactor it into something sane and readable someday.
            raise Exception, "\n\nSmoke Test suite failed for the following urls:\n%s\n\nWith:%s" % ("%s\n"%"".join([" - %s\n" % e["config"].url_name for e in exceptions]), ("".join(["%s:\n%s" % (e["config"].url_name, e["results"]) for e in exceptions])))
                
