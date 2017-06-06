from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from django.contrib.auth.models import User
from rest_framework.test import APIClient

from api.models import Sense, Artist, Place, Song, Domain, SemanticClass, Annotation, Dictionary, Example


class BaseApiTest(APITestCase):

    def setUp(self):
        self.user = User.objects.create(username="test", email="ad@min.com", password="admin", is_superuser=True)
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)


class SenseApiTest(BaseApiTest):

    url = reverse('sense-list')
    instance_url = url + "{}/"

    def test_POST_sense(self):

        data = {
            "owner": self.user.id,
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


class ArtistApiTest(BaseApiTest):

    url = reverse('artist-list')
    instance_url = url + "{}/"

    def test_POST_artist(self):

        data = {
            "owner": self.user.id,
            "name": "test artist",
            "annotations": [],
        }
        response = self.client.post(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Artist.objects.count(), 1)
        self.assertEqual(Artist.objects.get().name, 'test artist')


class PlaceApiTest(BaseApiTest):

    url = reverse('place-list')
    instance_url = url + "{}/"

    def test_POST_place(self):

        data = {
            "owner": self.user.id,
            "full_name": "test city, test state, test country",
            "annotations": [],
            "within": [],
            "artists": [],
        }
        response = self.client.post(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Place.objects.count(), 1)
        self.assertEqual(Place.objects.get().full_name, "test city, test state, test country")
        self.assertEqual(Place.objects.get().name, "test city")
