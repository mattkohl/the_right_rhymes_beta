from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from django.contrib.auth.models import User
from rest_framework.test import APIClient
from api.tests.test_models import BaseTest


class PermissionsTest(APITestCase):

    def test_unauthenticated_GET_all_senses(self):

        url = reverse('sense-list')
        client = APIClient()
        response = client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_unauthenticated_POST_new_sense(self):

        data = {
            "headword": "test sense",
            "part_of_speech": "noun",
            "definition": "test definition",
        }

        url = reverse('sense-list')
        client = APIClient()
        response = client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertIn("Authentication credentials were not provided", str(response.content))



