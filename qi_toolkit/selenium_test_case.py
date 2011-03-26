from djangosanetesting.cases import SeleniumTestCase
from django.core.management import call_command
from helpers import silence_print, unsilence_print
import time

class QiSeleniumTestCase(SeleniumTestCase):
    # selenium_fixtures = []
    
    def setUp(self, *args, **kwargs):
        self.verificationErrors = []

    def tearDown(self, *args, **kwargs):
        self.assertEqual([], self.verificationErrors)

    def js_refresh(self):
        sel = self.selenium
        sel.get_eval("window.location.href")
        sel.get_eval("window.location.href=window.location.href;")
        time.sleep(4)

class QiConservativeSeleniumTestCase(QiSeleniumTestCase):

    def tearDown(self, *args, **kwargs):
        super(QiConservativeSeleniumTestCase,self).tearDown(*args, **kwargs)
        _p = silence_print()
        call_command('flush', interactive=False)
        unsilence_print(_p)

