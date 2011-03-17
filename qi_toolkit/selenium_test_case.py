from djangosanetesting.cases import SeleniumTestCase
from django.core.management import call_command
from helpers import silence_print, unsilence_print
class QiSeleniumTestCase(SeleniumTestCase):
    selenium_fixtures = []
    
    def setUp(self, *args, **kwargs):
        self.verificationErrors = []
        super(QiSeleniumTestCase,self).setUp(*args, **kwargs)

    def tearDown(self, *args, **kwargs):
        self.assertEqual([], self.verificationErrors)
        super(QiSeleniumTestCase,self).tearDown(*args, **kwargs)

class QiConservativeSeleniumTestCase(QiSeleniumTestCase):

    def tearDown(self, *args, **kwargs):
        super(QiConservativeSeleniumTestCase,self).tearDown(*args, **kwargs)
        silence_print()
        call_command('flush', interactive=False)
        unsilence_print()

