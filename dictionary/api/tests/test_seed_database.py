from django.test import TestCase
from django.contrib.auth.models import User
from api.tests.test_models import BaseTest
from api.models import Sense, Artist, Song, Example, Place
from api.management.commands.seed_database import json_extract


class TestSeedDatabase(BaseTest):

    def test_sense_json_extract(self):

        sense_result = {
            "headword": "test headword",
            "part_of_speech": "noun",
            "definition": "test definition",
            "note": "test note",
            "etymology": "test etymology",
        }

        extracted = json_extract(sense_result, self.user, "sense")
        self.assertTrue("owner" in extracted)
        self.assertEqual(extracted['owner'], self.user)




