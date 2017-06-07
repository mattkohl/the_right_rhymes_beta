import time
import unittest
from selenium import webdriver
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


class NewVisitorTest(unittest.TestCase):

    def setUp(self):
        self.browser = webdriver.Firefox()

    def tearDown(self):
        self.browser.quit()

    def test_open_api_root_page(self):
        self.browser.get('http://localhost:8000/data/')
        self.assertIn("Api Root", self.browser.title)


if __name__ == '__main__':
    unittest.main(warnings='ignore')
