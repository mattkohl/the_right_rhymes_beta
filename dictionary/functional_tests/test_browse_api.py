from functional_tests.base import FunctionalTest


class NewVisitorTest(FunctionalTest):

    def test_open_api_root_page(self):
        self.browser.get(self.api_url)
        self.assertIn("Api Root", self.browser.title)

    def test_list_endpoints(self):
        self.browser.get(self.api_url)
        links = self.browser.find_elements_by_xpath('//div/pre/a')
        [self.assertRegex(element.text, "/[\w\-]+/") for element in links]