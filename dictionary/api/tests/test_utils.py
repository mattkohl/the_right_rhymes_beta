from unittest import TestCase
from api.utils import clean_up_date, slugify


class UtilTest(TestCase):

    def test_clean_up_date(self):
        year_only = "2001"
        year_only_cleaned = clean_up_date(year_only)
        self.assertEqual(year_only_cleaned, "2001-12-31")
        year_and_month = "2012-10"
        year_and_month_cleaned = clean_up_date(year_and_month)
        self.assertEqual(year_and_month_cleaned, "2012-10-31")
        year_and_feb = "1979-02"
        year_and_feb_cleaned = clean_up_date(year_and_feb)
        self.assertEqual(year_and_feb_cleaned, "1979-02-28")

    def test_slugify(self):
        pathological_case = "-a.b:c/d$e*f%g&h&amp;i+jklmnéóōo',?()pqrstá@uvwxyz½1234567890"
        result = "a-bcdsefpercentgandhandiandjklmneooopqrstaatuvwxyzhalf1234567890"
        self.assertEqual(slugify(pathological_case), result)
