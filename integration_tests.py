from selenium.webdriver.firefox.webdriver import WebDriver
from django.test import LiveServerTestCase


class IntegrationTests(LiveServerTestCase):
    @classmethod
    def setUpClass(cls):
        cls.selenium = WebDriver()
        cls.selenium.implicitly_wait(3)
        super(IntegrationTests, cls).setUpClass()

    @classmethod
    def tearDownClass(cls):
        cls.selenium.quit()
        super(IntegrationTests, cls).tearDownClass()

    def get(self, path, query=None):
        return self.selenium.get("{scheme_host_port}{path}".format(
            scheme_host_port=self.live_server_url,
            path=path
        ))

    def test_title(self):
        self.get('/')
        self.assertIn('Splatterpunk', self.selenium.title)
