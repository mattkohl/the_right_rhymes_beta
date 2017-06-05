from django.test import TestCase
from django.contrib.auth.models import User
from rest_framework.test import APIClient

from api.models import Sense, Artist, Place, Song, Domain, SemanticClass, Annotation, Dictionary, Example


class SenseAPITest(TestCase):

    def setUp(self):
        self.base_url = "/data/senses/"
        self.instance_url = self.base_url + "{}/"
        self.user = User.objects.create(username="test", email="ad@min.com", password="admin", is_superuser=True)
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)

    def test_sense_endpoint(self):

        data = {
            'owner': self.user.id,
            "headword": "test sense",
            "part_of_speech": "noun",
            "derives_from": [],
            "hyponyms": [],
            "holonyms": [],
            "annotations": [],
        }
        request = self.client.post("/data/senses/", data, format='json')
        self.assertEqual(request.status_code, 201)
        sense_count = Sense.objects.all().count()
        self.assertEqual(sense_count, 1)
