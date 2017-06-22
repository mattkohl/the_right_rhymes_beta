from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from django.contrib.auth.models import User
from rest_framework.test import APIClient
from api.tests.test_views import BaseApiTest
from api.models import Sense


class UnauthenticatedPermissionsTest(APITestCase):

    def setUp(self):
        self.client = APIClient()

    def test_unauthenticated_GET_all_senses(self):

        url = reverse('sense-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_unauthenticated_POST_new_sense(self):

        data = {
            "headword": "test sense",
            "part_of_speech": "noun",
            "definition": "test definition",
        }

        url = reverse('sense-list')
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertIn("Authentication credentials were not provided", str(response.content))


class AuthenticatedPermissionsTest(BaseApiTest):

    def test_authenticated_PUT_existing_sense(self):
        data = {
            "headword": "test sense",
            "part_of_speech": "noun",
            "definition": "test definition",
            "derives_from": [],
            "hyponyms": [],
            "holonyms": [],
            "annotations": [],
        }

        url = reverse('sense-list')
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        sense = Sense.objects.first()
        self.assertEqual(sense.part_of_speech, "noun")

        sense_url = response.data['url']
        data['part_of_speech'] = "adverb"
        response = self.client.put(sense_url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        sense = Sense.objects.first()
        self.assertEqual(sense.part_of_speech, "adverb")








