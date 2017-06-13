from api.tests.test_models import BaseTest
from api.utils import clean_up_date, slugify, extract_rhymes
from api.models import Annotation, Example, Song, Artist


class UtilTest(BaseTest):

    artist_data = {
        "name": "Test artist"
    }

    song_data = {
        "title": "Test song",
        "album": "Test album",
        "release_date": "2017-03-30",
    }

    example_data = {
        "text": "Cat in the hat"
    }

    def test_clean_up_date(self):
        year_only = "2001"
        year_only_cleaned = clean_up_date(year_only)
        self.assertEqual(year_only_cleaned, "2001-12-31")
        year_and_month = "2012-10"
        year_and_month_cleaned = clean_up_date(year_and_month)
        self.assertEqual(year_and_month_cleaned, "2012-10-31")
        year_and_feb = "1979-02"
        year_and_feb_cleaned = clean_up_date(year_and_feb)
        self.assertEqual(year_and_feb_cleaned, "1979-02-28")

    def test_slugify(self):
        pathological_case = "-a.b:c/d$e*f%g&h&amp;i+jklmnéóōo',?()pqrstá@uvwxyz½1234567890"
        result = "a-bcdsefpercentgandhandiandjklmneooopqrstaatuvwxyzhalf1234567890"
        self.assertEqual(slugify(pathological_case), result)

    def test_extract_rhymes(self):
        artist_ = Artist(owner=self.user, **self.artist_data)
        artist_.save()
        self.assertEqual(Artist.objects.count(), 1)
        song_ = Song(owner=self.user, **self.song_data)
        song_.save()
        song_.primary_artists.add(artist_)
        self.assertEqual(Song.objects.count(), 1)
        example_ = Example(owner=self.user, from_song=song_, **self.example_data)
        example_.save()
        example_.primary_artists.add(artist_)
        self.assertEqual(Example.objects.count(), 1)
        self.assertEqual(example_.from_song, song_)
        annotation_1 = Annotation(owner=self.user, text="Cat", offset=0, example=example_)
        annotation_1.save()
        annotation_2 = Annotation(owner=self.user, text="hat", offset=11, example=example_)
        annotation_2.save()
        self.assertEqual(Annotation.objects.count(), 2)
        annotation_1.rhymes.add(annotation_2)

        rhymes = extract_rhymes([annotation_1, annotation_2])
        self.assertTrue('right' in rhymes[0])
        self.assertTrue('left' in rhymes[0])
        self.assertIsInstance(rhymes[0]["right"], Annotation)
        self.assertIsInstance(rhymes[0]["left"], Annotation)
