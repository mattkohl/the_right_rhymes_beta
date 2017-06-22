from copy import deepcopy
from django.test import TestCase
from django.test.client import RequestFactory
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from api.models import Sense, Artist, Song, Example, Place


class BaseTest(TestCase):

    def setUp(self):
        self.user = User.objects.create(username="test", email="ad@min.com", password="admin", is_superuser=True)
        self.factory = RequestFactory()
        self.request = self.factory.get('/')
        self.host = self.request.get_host()


class SenseModelTest(BaseTest):

    first_data = {
        "definition": "The first (ever) sense",
        "headword": "test sense",
        "part_of_speech": "noun",
    }

    second_data = {
        "definition": "Sense the second",
        "headword": "test sense",
        "part_of_speech": "noun",
    }

    def test_saving_and_retrieving_senses(self):
        first_sense = Sense(owner=self.user, **self.first_data)
        first_sense.save()

        second_sense = Sense(owner=self.user, **self.second_data)
        second_sense.save()

        saved_senses = Sense.objects.all()
        self.assertEqual(saved_senses.count(), 2)

        first_saved_sense = saved_senses[0]
        second_saved_sense = saved_senses[1]
        self.assertEqual(first_saved_sense.definition, 'The first (ever) sense')
        self.assertEqual(second_saved_sense.definition, 'Sense the second')
        self.assertEqual(first_saved_sense.headword, second_saved_sense.headword)

    def test_cannot_save_sense_without_definition(self):
        copied = deepcopy(self.first_data)
        copied.pop("definition")
        sense = Sense(owner=self.user, **copied)
        with self.assertRaises(ValidationError):
            sense.save()
            sense.full_clean()

    def test_cannot_save_sense_without_part_of_speech(self):
        copied = deepcopy(self.first_data)
        copied.pop("part_of_speech")
        sense = Sense(owner=self.user, **copied)
        with self.assertRaises(ValidationError):
            sense.save()
            sense.full_clean()

    def test_cannot_save_sense_without_headword(self):
        copied = deepcopy(self.first_data)
        copied.pop("headword")
        sense = Sense(owner=self.user, **copied)
        with self.assertRaises(ValidationError):
            sense.save()
            sense.full_clean()


class ArtistModelTest(BaseTest):

    data = {
        "name": "Test artist"
    }

    def test_saving_and_retrieving_artists(self):
        artist_ = Artist(owner=self.user, **self.data)
        artist_.save()
        self.assertEqual(Artist.objects.count(), 1)
        self.assertEqual(artist_, Artist.objects.first())
        
    def test_cannot_save_artist_without_name(self):
        copied = deepcopy(self.data)
        copied.pop("name")
        artist = Artist(owner=self.user, **copied)
        with self.assertRaises(ValidationError):
            artist.save()
            artist.full_clean()


class PlaceModelTest(BaseTest):

    data = {
        "full_name": "City, State, Country",
    }

    lat_lng = {
        "latitude": 1,
        "longitude": 2,
    }

    def test_saving_and_retrieving_places(self):
        place = Place(owner=self.user, **self.data)
        place.save()
        self.assertEqual(Place.objects.count(), 1)
        self.assertEqual(place, Place.objects.first())

    def test_add_artist(self):
        artist = Artist(owner=self.user, name="test artist")
        artist.save()
        place = Place(owner=self.user, **self.data)
        place.save()
        place.artists.add(artist)
        self.assertEqual(place.artists.count(), 1)
        self.assertEqual(place.artists.first().name, "test artist")
        
    def test_cannot_save_place_without_full_name(self):
        copied = deepcopy(self.data)
        copied.pop("full_name")
        place = Place(owner=self.user, **copied)
        with self.assertRaises(ValidationError):
            place.save()
            place.full_clean()


class SongModelTest(BaseTest):

    artist_data = {
        "name": "Test artist"
    }

    song_data = {
        "title": "Test song",
        "album": "Test album",
        "release_date": "2017-03-30",
    }

    def test_saving_and_retrieving_songs(self):
        artist = Artist(owner=self.user, **self.artist_data)
        artist.save()
        song = Song(owner=self.user, **self.song_data)
        song.save()
        song.primary_artists.add(artist)
        self.assertEqual(Song.objects.count(), 1)
        self.assertEqual(song, Song.objects.first())
        self.assertEqual(song.primary_artists.count(), 1)
        self.assertEqual(song.primary_artists.first().name, "Test artist")
        
    def test_cannot_save_song_without_title(self):
        copied = deepcopy(self.song_data)
        copied.pop("title")
        song = Song(owner=self.user, **copied)
        with self.assertRaises(ValidationError):
            song.save()
            song.full_clean()

    def test_cannot_save_song_without_album(self):
        copied = deepcopy(self.song_data)
        copied.pop("album")
        song = Song(owner=self.user, **copied)
        with self.assertRaises(ValidationError):
            song.save()
            song.full_clean()

    def test_cannot_save_song_with_invalid_date(self):
        copied = deepcopy(self.song_data)
        copied["release_date"] = "bounce with me"
        song = Song(owner=self.user, **copied)
        with self.assertRaises(ValidationError):
            song.save()
            song.full_clean()
