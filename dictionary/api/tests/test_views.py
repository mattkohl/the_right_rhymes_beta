from datetime import date
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from django.contrib.auth.models import User
from rest_framework.test import APIClient
from django.test.client import RequestFactory

from api.models import Sense, Artist, Place, Song, Domain, SemanticClass, Annotation, Dictionary, Example
from api.utils import make_uri

###
# coverage run --source='.' manage.py test api
###


class BaseApiTest(APITestCase):

    def setUp(self):
        self.user = User.objects.create(username="test", email="ad@min.com", password="admin", is_superuser=True)
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)
        self.factory = RequestFactory()
        self.request = self.factory.get('/')
        self.host = self.request.get_host()


class DictionaryApiTest(BaseApiTest):

    url = reverse('dictionary-list')
    data = {
        "name": "test dictionary",
    }

    def test_POST_dictionary(self):
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
        response = self.client.post(self.url, self.data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Sense.objects.count(), 1)
        self.assertEqual(Sense.objects.get().headword, 'test sense')

    def test_GET_sense(self):
        self.client.post(self.url, self.data, format='json')
        response = self.client.get(self.url, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['count'], 1)
        sense_ = response.data['results'][0]
        self.assertEqual(sense_['headword'], self.data['headword'])
        self.assertEqual(sense_['part_of_speech'], self.data['part_of_speech'])


class ArtistApiTest(BaseApiTest):

    url = reverse('artist-list')
    data = {
        "name": "test artist",
        "annotations": [],
    }

    def test_POST_artist(self):
        response = self.client.post(self.url, self.data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Artist.objects.count(), 1)
        self.assertEqual(Artist.objects.get().name, 'test artist')

    def test_GET_artist(self):
        self.client.post(self.url, self.data, format='json')
        response = self.client.get(self.url, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['count'], 1)
        artist_ = response.data['results'][0]
        self.assertEqual(artist_['name'], self.data['name'])


class PlaceApiTest(BaseApiTest):

    url = reverse('place-list')
    data = {
        "full_name": "test city, test state, test country",
        "annotations": [],
        "within": [],
        "artists": [],
    }

    def test_POST_place(self):
        response = self.client.post(self.url, self.data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Place.objects.count(), 1)
        self.assertEqual(Place.objects.get().full_name, "test city, test state, test country")
        self.assertEqual(Place.objects.get().name, "test city")

    def test_GET_place(self):
        self.client.post(self.url, self.data, format='json')
        response = self.client.get(self.url, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['count'], 1)
        place_ = response.data['results'][0]
        self.assertEqual(place_['full_name'], self.data['full_name'])


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
        test_artist_uri = make_uri(self.host, 'artists', test_artist.id)

        self.song_data.update({"primary_artists": [test_artist_uri]})
        response = self.client.post(self.url, self.song_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Song.objects.count(), 1)
        self.assertEqual(Song.objects.get().title, "test song")
        self.assertEqual(Song.objects.get().release_date, date(2001, 12, 31))

    def test_GET_song(self):
        response = self.client.post(self.artist_url, self.artist_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Artist.objects.count(), 1)
        test_artist = Artist.objects.get()
        test_artist_uri = make_uri(self.host, 'artists', test_artist.id)

        self.song_data.update({"primary_artists": [test_artist_uri]})
        self.client.post(self.url, self.song_data, format='json')

        response = self.client.get(self.url, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['count'], 1)
        song_ = response.data['results'][0]
        self.assertEqual(song_['title'], self.song_data['title'])


class ExampleApiTest(BaseApiTest):

    artist_url = reverse('artist-list')
    artist_data = {
        "name": "test artist",
        "annotations": [],
    }

    song_url = reverse('song-list')
    song_data = {
        "title": "test song",
        "release_date_string": "2001-10-12",
        "album": "test album",
        "annotations": [],
        "featured_artists": [],
        "examples": []
    }

    example_url = reverse('example-list')
    example_data = {
        'text': "This is a test example",
        'annotations': []
    }

    def test_POST_example(self):
        self.client.post(self.artist_url, self.artist_data)
        test_artist = Artist.objects.get()
        test_artist_uri = make_uri(self.host, 'artists', test_artist.id)

        self.song_data.update({"primary_artists": [test_artist_uri]})
        self.client.post(self.song_url, self.song_data, format='json')
        test_song = Song.objects.get()
        test_song_uri = make_uri(self.host, 'songs', test_song.id)

        self.example_data.update({"primary_artists": [test_artist_uri], "from_song": test_song_uri})
        response = self.client.post(self.example_url, self.example_data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_GET_example(self):
        self.client.post(self.artist_url, self.artist_data)
        test_artist = Artist.objects.get()
        test_artist_uri = make_uri(self.host, 'artists', test_artist.id)

        self.song_data.update({"primary_artists": [test_artist_uri]})
        self.client.post(self.song_url, self.song_data, format='json')
        test_song = Song.objects.get()
        test_song_uri = make_uri(self.host, 'songs', test_song.id)

        self.example_data.update({"primary_artists": [test_artist_uri], "from_song": test_song_uri})
        self.client.post(self.example_url, self.example_data, format="json")

        response = self.client.get(self.example_url, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['count'], 1)
        example_ = response.data['results'][0]
        self.assertEqual(example_['text'], self.example_data['text'])
        test_example = Example.objects.get()
        self.assertEqual(example_['text'], test_example.text)
