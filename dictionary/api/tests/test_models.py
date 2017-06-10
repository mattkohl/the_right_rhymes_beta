from django.test import TestCase
from django.contrib.auth.models import User
from api.models import Sense, Artist, Song, Example, Place


class BaseTest(TestCase):

    def setUp(self):
        self.user = User.objects.create(username="test", email="ad@min.com", password="admin", is_superuser=True)


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


class ArtistModelTest(BaseTest):

    data = {
        "name": "Test artist"
    }

    def test_saving_and_retrieving_artists(self):
        artist_ = Artist(owner=self.user, **self.data)
        artist_.save()
        self.assertEqual(Artist.objects.count(), 1)
        self.assertEqual(artist_, Artist.objects.first())


class PlaceModelTest(BaseTest):

    data = {
        "full_name": "City, State, Country",
    }

    lat_lng = {
        "latitude": 1,
        "longitude": 2,
    }

    def test_saving_and_retrieving_places(self):
        place_ = Place(owner=self.user, **self.data)
        place_.save()
        self.assertEqual(Place.objects.count(), 1)
        self.assertEqual(place_, Place.objects.first())

    def test_add_artist(self):
        artist_ = Artist(owner=self.user, name="test artist")
        artist_.save()
        place_ = Place(owner=self.user, **self.data)
        place_.save()
        place_.artists.add(artist_)
        self.assertEqual(place_.artists.count(), 1)
        self.assertEqual(place_.artists.first().name, "test artist")
