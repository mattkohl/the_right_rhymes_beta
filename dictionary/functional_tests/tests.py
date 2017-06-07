import time
from django.test import LiveServerTestCase
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import WebDriverException


MAX_WAIT = 10


def wait(fn):
    def modified_fn(*args, **kwargs):
        start_time = time.time()
        while True:
            try:
                return fn(*args, **kwargs)
            except (AssertionError, WebDriverException) as e:
                if time.time() - start_time > MAX_WAIT:
                    raise e
                time.sleep(0.5)
    return modified_fn


class NewVisitorTest(LiveServerTestCase):

    def setUp(self):
        self.browser = webdriver.Firefox()
        self.api_url = self.live_server_url + "/data/"

    def tearDown(self):
        self.browser.quit()

    def test_open_api_root_page(self):
        self.browser.get(self.api_url)
        self.assertIn("Api Root", self.browser.title)

    def test_list_endpoints(self):
        self.browser.get(self.api_url)
        links = self.browser.find_elements_by_xpath('//div/pre/a')
        [self.assertRegex(element.text, "/data/[\w\-]+/") for element in links]

