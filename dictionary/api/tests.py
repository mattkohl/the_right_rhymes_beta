from django.test import TestCase
from django.contrib.auth.models import User
from rest_framework.test import APIClient

from api.models import Sense, Artist, Place, Song, Domain, SemanticClass, Annotation, Dictionary, Example


# class DictionaryAPITest(TestCase):
#
#     base_url = "/data/dictionaries/{}/"
#
#     def test_get_returns_200(self):
#         user_ = User.objects.create(username="test", email="ad@min.com", password="admin")
#         dictionary_ = Dictionary.objects.create(owner=user_)
#         response = self.client.get(self.base_url.format(dictionary_.id))
#         self.assertEqual(response.status_code, 200)
#         self.assertEqual(response['content-type'], 'application/json')
#
#     def test_dictionary_endpoint(self):
#         user_ = User.objects.create(username="test", email="ad@min.com", password="admin")
#         factory = APIRequestFactory()
#         request = factory.post("/data/dictionaries/", {'owner': user_.id, "name": "Test Dictionary"}, format='json')
#         print(request)
#         dictionary_count = Dictionary.objects.all().count()
#         self.assertEqual(dictionary_count, 1)


class SenseAPITest(TestCase):

    base_url = "/data/senses/{}/"

    def test_sense_endpoint(self):
        user_ = User.objects.create(username="test", email="ad@min.com", password="admin", is_superuser=True)
        client = APIClient()
        client.force_authenticate(user=user_)
        data = {
            'owner': user_.id,
            "headword": "test sense",
            "part_of_speech": "noun",
            "derives_from": [],
            "hyponyms": [],
            "holonyms": [],
            "annotations": [],
        }
        request = client.post("/data/senses/", data, format='json')
        self.assertEqual(request.status_code, 201)
        sense_count = Sense.objects.all().count()
        self.assertEqual(sense_count, 1)

