from datetime import date
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from django.contrib.auth.models import User
from rest_framework.test import APIClient
from django.test.client import RequestFactory

from api.models import Sense, Artist, Place, Song, Domain, SemanticClass, Annotation, Dictionary, Example
from api.utils import make_uri


class BaseApiTest(APITestCase):

    def setUp(self):
        self.user = User.objects.create(username="test", email="ad@min.com", password="admin", is_superuser=True)
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)
        self.factory = RequestFactory()


class DictionaryApiTest(BaseApiTest):

    url = reverse('dictionary-list')
    data = {
        "name": "test dictionary",
    }

    def test_POST_dictionary(self):
        self.data['owner'] = self.user.id
        response = self.client.post(self.url, self.data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Dictionary.objects.count(), 1)
        self.assertEqual(Dictionary.objects.get().name, 'test dictionary')


class SenseApiTest(BaseApiTest):

    url = reverse('sense-list')

    data = {
        "headword": "test sense",
        "part_of_speech": "noun",
        "derives_from": [],
        "hyponyms": [],
        "holonyms": [],
        "annotations": [],
    }

    def test_POST_sense(self):
        self.data['owner'] = self.user.id
        response = self.client.post(self.url, self.data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Sense.objects.count(), 1)
        self.assertEqual(Sense.objects.get().headword, 'test sense')

    def test_GET_sense(self):
        self.data['owner'] = self.user.id
        self.client.post(self.url, self.data, format='json')
        response = self.client.get(self.url, format="json")
        self.assertEqual(response.data['count'], 1)


class ArtistApiTest(BaseApiTest):

    url = reverse('artist-list')
    data = {
        "name": "test artist",
        "annotations": [],
    }

    def test_POST_artist(self):
        self.data['owner'] = self.user.id
        response = self.client.post(self.url, self.data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Artist.objects.count(), 1)
        self.assertEqual(Artist.objects.get().name, 'test artist')


class PlaceApiTest(BaseApiTest):

    url = reverse('place-list')
    data = {
        "full_name": "test city, test state, test country",
        "annotations": [],
        "within": [],
        "artists": [],
    }

    def test_POST_place(self):
        self.data['owner'] = self.user.id
        response = self.client.post(self.url, self.data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Place.objects.count(), 1)
        self.assertEqual(Place.objects.get().full_name, "test city, test state, test country")
        self.assertEqual(Place.objects.get().name, "test city")


class SongApiTest(BaseApiTest):

    url = reverse('song-list')
    artist_url = reverse('artist-list')

    artist_data = {
        "name": "test artist",
        "annotations": [],
    }

    song_data = {
        "title": "test song",
        "release_date_string": "2001",
        "album": "test album",
        "annotations": [],
        "featured_artists": [],
        "examples": []
    }

    def test_POST_song(self):

        response = self.client.post(self.artist_url, self.artist_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Artist.objects.count(), 1)
        test_artist = Artist.objects.get()
        request = self.factory.get('/data/')
        host = request.get_host()
        test_artist_uri = make_uri(host, 'artists', test_artist.id)
        self.song_data.update({"primary_artists": [test_artist_uri], "owner": self.user.id})

        self.song_data['owner'] = self.user.id
        response = self.client.post(self.url, self.song_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Song.objects.count(), 1)
        self.assertEqual(Song.objects.get().title, "test song")
        self.assertEqual(Song.objects.get().release_date, date(2001, 12, 31))


