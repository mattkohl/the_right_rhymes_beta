from datetime import date
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from rest_framework.authtoken.models import Token
from django.contrib.auth.models import User
from rest_framework.test import APIClient
from django.test.client import RequestFactory

from api.models import Sense, Artist, Place, Song, Domain, SemanticClass, Annotation, Dictionary, Example
from api.forms import ArtistForm, PlaceForm
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
        self.token, self.token_created = Token.objects.get_or_create(user=self.user)


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

    list_url = reverse('sense-list')
    search_url = reverse('sense-search')
    detail_url = reverse('sense-detail', kwargs={'pk': 1})
    highlight_url = reverse('sense-highlight', kwargs={'pk': 1})

    data = {
        "headword": "test sense",
        "part_of_speech": "noun",
        "definition": "test definition",
        "derives_from": [],
        "hyponyms": [],
        "holonyms": [],
        "annotations": [],
    }

    def test_POST_a_sense(self):
        response = self.client.post(self.list_url, self.data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Sense.objects.count(), 1)
        self.assertEqual(Sense.objects.get().headword, 'test sense')

    def test_GET_list_all_senses(self):
        self.create_a_sense()
        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['count'], 1)

    def create_a_sense(self):
        self.client.post(self.list_url, self.data, format='json')

    def test_GET_search_all_senses(self):
        self.create_a_sense()
        response = self.client.get(self.search_url, {"q": "test"})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['senses'].count(), 1)
        sense_ = response.data['senses'].first()
        self.assertEqual(sense_.headword, self.data['headword'])
        self.assertEqual(sense_.part_of_speech, self.data['part_of_speech'])

    def test_GET_a_sense(self):
        self.create_a_sense()
        response = self.client.get(self.detail_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_GET_a_sense_highlight(self):
        self.create_a_sense()
        response = self.client.get(self.highlight_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class ArtistApiTest(BaseApiTest):

    list_url = reverse('artist-list')
    search_url = reverse('artist-search')
    detail_url = reverse('artist-detail', kwargs={'pk': 1})
    highlight_url = reverse('artist-highlight', kwargs={'pk': 1})
    
    data = {
        "name": "test artist",
        "annotations": [],
    }

    def test_POST_an_artist(self):
        response = self.client.post(self.list_url, self.data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Artist.objects.count(), 1)
        self.assertEqual(Artist.objects.get().name, 'test artist')

    def test_GET_all_artists(self):
        self.create_an_artist()
        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['count'], 1)

    def create_an_artist(self):
        self.client.post(self.list_url, self.data, format='json')

    def test_GET_search_all_artists(self):
        self.create_an_artist()
        response = self.client.get(self.search_url, {"q": "test"})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['artists'].count(), 1)
        artist_ = response.data['artists'].first()
        self.assertEqual(artist_.name, self.data['name'])

    def test_GET_search_all_artists_uses_artist_form(self):
        response = self.client.get(self.search_url)
        self.assertIsInstance(response.context['form'], ArtistForm)

    def test_GET_an_artist(self):
        self.create_an_artist()
        response = self.client.get(self.detail_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_GET_an_artist_highlight(self):
        self.create_an_artist()
        response = self.client.get(self.highlight_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class PlaceApiTest(BaseApiTest):

    list_url = reverse('place-list')
    search_url = reverse('place-search')
    detail_url = reverse('place-detail', kwargs={'pk': 1})
    highlight_url = reverse('place-highlight', kwargs={'pk': 1})
    data = {
        "full_name": "test city, test state, test country",
        "annotations": [],
        "within": [],
        "artists": [],
    }

    def test_POST_a_place(self):
        response = self.client.post(self.list_url, self.data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Place.objects.count(), 1)
        self.assertEqual(Place.objects.get().full_name, "test city, test state, test country")
        self.assertEqual(Place.objects.get().name, "test city")

    def test_GET_all_places(self):
        self.create_a_place()
        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['count'], 1)

    def create_a_place(self):
        self.client.post(self.list_url, self.data, format='json')

    def test_GET_search_all_places(self):
        self.create_a_place()
        response = self.client.get(self.search_url, {"q": "test"})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['places'].count(), 1)
        place_ = response.data['places'].first()
        self.assertEqual(place_.full_name, self.data['full_name'])

    def test_GET_a_place(self):
        self.create_a_place()
        response = self.client.get(self.detail_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_GET_a_place_highlight(self):
        self.create_a_place()
        response = self.client.get(self.highlight_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class SongApiTest(BaseApiTest):

    list_url = reverse('song-list')
    search_url = reverse('song-search')
    detail_url = reverse('song-detail', kwargs={'pk': 1})
    highlight_url = reverse('song-highlight', kwargs={'pk': 1})
    artist_list_url = reverse('artist-list')

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
        "examples": [],
        "lyrics": "test lyrics",
    }

    def test_POST_a_song(self):

        response = self.client.post(self.artist_list_url, self.artist_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Artist.objects.count(), 1)
        test_artist = Artist.objects.get()
        test_artist_uri = make_uri(self.host, 'artists', test_artist.id)

        self.song_data.update({"primary_artists": [test_artist_uri]})
        response = self.client.post(self.list_url, self.song_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Song.objects.count(), 1)
        self.assertEqual(Song.objects.get().title, "test song")
        self.assertEqual(Song.objects.get().release_date, date(2001, 12, 31))

    def test_GET_all_songs(self):
        self.create_a_song()

        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['count'], 1)

    def create_a_song(self):
        response = self.client.post(self.artist_list_url, self.artist_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Artist.objects.count(), 1)
        test_artist = Artist.objects.get()
        test_artist_uri = make_uri(self.host, 'artists', test_artist.id)
        self.song_data.update({"primary_artists": [test_artist_uri]})
        self.client.post(self.list_url, self.song_data, format='json')

    def test_GET_search_all_songs(self):
        self.create_a_song()
        response = self.client.get(self.search_url, {"q": "test"})
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # TODO: change this API? all the other responses are querysets
        self.assertEqual(len(response.data['song_titles']), 1)
        song_ = response.data['song_titles'][0]
        self.assertEqual(song_["title"], self.song_data['title'])

    def test_GET_a_song(self):
        self.create_a_song()
        response = self.client.get(self.detail_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_GET_a_song_highlight(self):
        self.create_a_song()
        response = self.client.get(self.highlight_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class ExampleApiTest(BaseApiTest):

    artist_list_url = reverse('artist-list')
    artist_data = {
        "name": "test artist",
        "annotations": [],
    }

    song_list_url = reverse('song-list')
    song_data = {
        "title": "test song",
        "release_date_string": "2001-10-12",
        "album": "test album",
        "annotations": [],
        "featured_artists": [],
        "examples": []
    }

    list_url = reverse('example-list')
    search_url = reverse('example-search')
    detail_url = reverse('example-detail', kwargs={'pk': 1})
    highlight_url = reverse('example-highlight', kwargs={'pk': 1})
    example_data = {
        'text': "This is a test example",
        'annotations': []
    }

    def test_POST_example(self):
        self.client.post(self.artist_list_url, self.artist_data)
        test_artist = Artist.objects.get()
        test_artist_uri = make_uri(self.host, 'artists', test_artist.id)

        self.song_data.update({"primary_artists": [test_artist_uri]})
        self.client.post(self.song_list_url, self.song_data, format='json')
        test_song = Song.objects.get()
        test_song_uri = make_uri(self.host, 'songs', test_song.id)

        self.example_data.update({"primary_artists": [test_artist_uri], "from_song": test_song_uri})
        response = self.client.post(self.list_url, self.example_data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_GET_example(self):
        self.client.post(self.artist_list_url, self.artist_data)
        test_artist = Artist.objects.get()
        test_artist_uri = make_uri(self.host, 'artists', test_artist.id)

        self.song_data.update({"primary_artists": [test_artist_uri]})
        self.client.post(self.song_list_url, self.song_data, format='json')
        test_song = Song.objects.get()
        test_song_uri = make_uri(self.host, 'songs', test_song.id)

        self.example_data.update({"primary_artists": [test_artist_uri], "from_song": test_song_uri})
        self.client.post(self.list_url, self.example_data, format="json")

        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['count'], 1)
        example_ = response.data['results'][0]
        self.assertEqual(example_['text'], self.example_data['text'])
        test_example = Example.objects.get()
        self.assertEqual(example_['text'], test_example.text)


class AnnotationApiTest(BaseApiTest):

    list_url = reverse('annotation-list')
    search_url = reverse('annotation-search')
    detail_url = reverse('annotation-detail', kwargs={'pk': 1})
    highlight_url = reverse('annotation-highlight', kwargs={'pk': 1})
    data = {
        "text": "test annotation",
        "offset": 0
    }

    artist_list_url = reverse('artist-list')
    artist_data = {
        "name": "test artist",
        "annotations": [],
    }

    song_list_url = reverse('song-list')
    song_data = {
        "title": "test song",
        "release_date_string": "2001-10-12",
        "album": "test album",
        "annotations": [],
        "featured_artists": [],
        "examples": []
    }

    example_list_url = reverse('example-list')
    example_data = {
        'text': "This is a test example",
        'annotations': []
    }

    def test_POST_annotation(self):
        self.client.post(self.artist_list_url, self.artist_data)
        test_artist = Artist.objects.get()
        test_artist_uri = make_uri(self.host, 'artists', test_artist.id)

        self.song_data.update({"primary_artists": [test_artist_uri]})
        self.client.post(self.song_list_url, self.song_data, format='json')
        test_song = Song.objects.get()
        test_song_uri = make_uri(self.host, 'songs', test_song.id)

        self.example_data.update({"primary_artists": [test_artist_uri], "from_song": test_song_uri})
        response = self.client.post(self.example_list_url, self.example_data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        test_example = Example.objects.get()
        test_example_uri = make_uri(self.host, 'examples', test_example.id)
        self.data['example'] = test_example_uri

        response = self.client.post(self.list_url, self.data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Annotation.objects.count(), 1)
        self.assertEqual(Annotation.objects.get().text, 'test annotation')


class DomainApiTest(BaseApiTest):
    list_url = reverse('domain-list')
    search_url = reverse('domain-search')
    detail_url = reverse('domain-detail', kwargs={'pk': 1})
    highlight_url = reverse('domain-highlight', kwargs={'pk': 1})

    data = {
        "name": "test domain",
        "narrower": []
    }

    def test_POST_a_domain(self):
        response = self.client.post(self.list_url, self.data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Domain.objects.count(), 1)
        self.assertEqual(Domain.objects.get().name, 'test domain')

    def test_GET_all_domains(self):
        self.create_a_domain()
        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['count'], 1)

    def create_a_domain(self):
        self.client.post(self.list_url, self.data, format='json')

    def test_GET_search_all_domains(self):
        self.create_a_domain()
        response = self.client.get(self.search_url, {"q": "test"})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['domains'].count(), 1)
        domain_ = response.data['domains'].first()
        self.assertEqual(domain_.name, self.data['name'])

    def test_GET_a_domain(self):
        self.create_a_domain()
        response = self.client.get(self.detail_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_GET_a_domain_highlight(self):
        self.create_a_domain()
        response = self.client.get(self.highlight_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class SemanticClassApiTest(BaseApiTest):
    list_url = reverse('semanticclass-list')
    search_url = reverse('semanticclass-search')
    detail_url = reverse('semanticclass-detail', kwargs={'pk': 1})
    highlight_url = reverse('semanticclass-highlight', kwargs={'pk': 1})

    data = {
        "name": "test semantic class",
        "narrower": []
    }

    def test_POST_a_semantic_class(self):
        response = self.client.post(self.list_url, self.data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(SemanticClass.objects.count(), 1)
        self.assertEqual(SemanticClass.objects.get().name, 'test semantic class')

    def test_GET_all_semantic_classes(self):
        self.create_a_semantic_class()
        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['count'], 1)

    def create_a_semantic_class(self):
        self.client.post(self.list_url, self.data, format='json')

    def test_GET_search_all_semantic_classes(self):
        self.create_a_semantic_class()
        response = self.client.get(self.search_url, {"q": "test"})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['semantic_classes'].count(), 1)
        semantic_class_ = response.data['semantic_classes'].first()
        self.assertEqual(semantic_class_.name, self.data['name'])

    def test_GET_a_semantic_class(self):
        self.create_a_semantic_class()
        response = self.client.get(self.detail_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_GET_a_semantic_class_highlight(self):
        self.create_a_semantic_class()
        response = self.client.get(self.highlight_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
