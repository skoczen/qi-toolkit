try:
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

    class QiConservativeSeleniumTestCase(SeleniumTestCase):
        selenium_fixtures = []
        
        def setUp(self, *args, **kwargs):
            self.verificationErrors = []
            super(QiSeleniumTestCase,self).setUp(*args, **kwargs)

        def tearDown(self, *args, **kwargs):
            self.assertEqual([], self.verificationErrors)
            silence_print()
            call_command('flush', interactive=False)
            unsilence_print()
            super(QiSeleniumTestCase,self).tearDown(*args, **kwargs)

except:
    pass