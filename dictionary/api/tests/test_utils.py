from unittest import TestCase
from api.utils import clean_up_date


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
