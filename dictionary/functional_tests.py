import unittest
from selenium import webdriver


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
