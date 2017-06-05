from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from django.contrib.auth.models import User
from rest_framework.test import APIClient

from api.models import Sense, Artist, Place, Song, Domain, SemanticClass, Annotation, Dictionary, Example


class SenseAPITest(APITestCase):

    def setUp(self):
        self.url = reverse('sense-list')
        self.instance_url = self.url + "{}/"
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
        response = self.client.post(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Sense.objects.count(), 1)
        self.assertEqual(Sense.objects.get().headword, 'test sense')
