try:
    from djangosanetesting.cases import SeleniumTestCase
    class QiSeleniumTestCase(SeleniumTestCase):
        selenium_fixtures = []
        
        def setUp(self, *args, **kwargs):
            self.verificationErrors = []
            super(QiSeleniumTestCase,self).setUp(*args, **kwargs)

        def tearDown(self, *args, **kwargs):
            self.assertEqual([], self.verificationErrors)
            super(QiSeleniumTestCase,self).tearDown(*args, **kwargs)

except:
    pass