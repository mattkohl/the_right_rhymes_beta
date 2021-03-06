from api.tests.test_models import BaseTest
from api.serializers import AnnotationSerializer, ExampleSerializer
from api.utils import clean_up_date, slugify, extract_rhymes, \
    build_example_serializer, build_annotation_serializer, \
    serialize_examples, clean_text, render_example_with_annotations, \
    build_annotation_link, build_songs_from_queryset, build_examples_from_queryset, \
    build_examples_from_annotations
from api.models import Annotation, Example, Song, Artist, Place, Sense


class UtilTest(BaseTest):

    artist_data = {
        "name": "Test artist"
    }

    place_data = {
        "full_name": "test city, test state, test country"
    }
    
    sense_data = {
        "definition": "test definition",
        "headword": "Test headword",
        "part_of_speech": "noun"
    }

    song_data = {
        "title": "Test song",
        "album": "Test album",
        "release_date": "2017-03-30",
        "lyrics": "Cat in the hat\n This song is about the cat in the hat\n",
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
        artist_ = self.create_an_artist()
        song_ = self.create_a_song(artist_)
        example_ = self.create_an_example(song_, artist_)
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

    def create_an_example(self, song_, artist_):
        example_ = Example(owner=self.user, from_song=song_, **self.example_data)
        example_.save()
        example_.primary_artists.add(artist_)
        return example_

    def create_a_song(self, artist_):
        song_ = Song(owner=self.user, **self.song_data)
        song_.save()
        song_.primary_artists.add(artist_)
        return song_

    def create_an_artist(self):
        artist_ = Artist(owner=self.user, **self.artist_data)
        artist_.save()
        return artist_

    def create_a_place(self):
        place_ = Place(owner=self.user, **self.place_data)
        place_.save()
        return place_

    def create_a_sense(self):
        sense_ = Sense(owner=self.user, **self.sense_data)
        sense_.save()
        return sense_

    def test_build_annotation_serializer(self):
        artist_ = self.create_an_artist()
        song_ = self.create_a_song(artist_)
        example_ = self.create_an_example(song_, artist_)
        annotation_serializer_ = build_annotation_serializer(self.request, example_, "Cat", 0)
        self.assertIsInstance(annotation_serializer_, AnnotationSerializer)
        self.assertEqual(annotation_serializer_.validated_data['example'], example_)

    def test_build_example_serializer(self):
        artist_ = self.create_an_artist()
        song_ = self.create_a_song(artist_)
        example_serializer_ = build_example_serializer(self.request, song_, "Cat in the hat")
        self.assertIsInstance(example_serializer_, ExampleSerializer)
        self.assertEqual(example_serializer_.validated_data['from_song'], song_)

    def test_serialize_examples(self):
        artist_ = self.create_an_artist()
        song_ = self.create_a_song(artist_)
        q = "hat"
        examples = serialize_examples(self.request, song_, q)
        self.assertEqual(len(examples), song_.lyrics.count(q))
        self.assertEqual(Example.objects.count(), 0)

    def test_clean_text(self):
        bad_apostrophe = "All this bread can’t be too good for my cholesterol"
        okay_apostrophe = "All this bread can't be too good for my cholesterol"
        cleaned = clean_text(bad_apostrophe)
        self.assertEqual(cleaned, okay_apostrophe)

    def test_build_annotation_link(self):
        artist_ = self.create_an_artist()
        place_ = self.create_a_place()
        sense_ = self.create_a_sense()
        song_ = self.create_a_song(artist_)
        example_ = self.create_an_example(song_, artist_)
        cat = Annotation(text="Cat", offset=example_.text.index("Cat"), example=example_, sense=sense_, owner=self.user)
        link = build_annotation_link(self.host, cat)
        self.assertEqual(link, '<a href="http://testserver/senses/1/">Cat</a>')
        cat.sense = None
        cat.artist = artist_
        cat.save()
        link = build_annotation_link(self.host, cat)
        self.assertEqual(link, '<a href="http://testserver/artists/1/">Cat</a>')
        cat.artist = None
        cat.place = place_
        cat.save()
        link = build_annotation_link(self.host, cat)
        self.assertEqual(link, '<a href="http://testserver/places/1/">Cat</a>')
        cat.place = None
        link = build_annotation_link(self.host, cat)
        self.assertEqual(link, '<span>Cat</span>')

    def test_render_example_with_annotations(self):
        artist_ = self.create_an_artist()
        place_ = self.create_a_place()
        sense_ = self.create_a_sense()
        song_ = self.create_a_song(artist_)
        example_ = self.create_an_example(song_, artist_)
        cat = Annotation(text="Cat", offset=example_.text.index("Cat"), example=example_, sense=sense_, owner=self.user)
        cat.save()
        the = Annotation(text="the", offset=example_.text.index("the"), example=example_, place=place_, owner=self.user)
        the.save()
        hat = Annotation(text="hat", offset=example_.text.index("hat"), example=example_, owner=self.user)
        hat.save()
        rendered = '<a href="http://testserver/senses/1/">Cat</a> in <a href="http://testserver/places/1/">the</a> <span>hat</span>'
        result = render_example_with_annotations(self.request, example_)
        self.assertEqual(result, rendered)

    def test_build_songs_from_queryset(self):
        artist_ = self.create_an_artist()
        song_ = self.create_a_song(artist_)
        self.create_an_example(song_, artist_)
        queryset = Song.objects.all()
        results_no_examples = build_songs_from_queryset(queryset, self.request, None)
        self.assertEqual(len(results_no_examples), 1)
        self.assertEqual(len(results_no_examples[0]['examples']), 0)

        results_with_all_examples = build_songs_from_queryset(queryset, self.request, "")
        self.assertEqual(len(results_with_all_examples), 1)
        self.assertEqual(len(results_with_all_examples[0]['examples']), 1)

        q = "non-matching filter"
        results_with_filtered_examples = build_songs_from_queryset(queryset, self.request, q)
        self.assertEqual(len(results_with_filtered_examples), 1)
        self.assertEqual(len(results_with_filtered_examples[0]['examples']), 0)

        q = "Cat"
        results_with_filtered_examples = build_songs_from_queryset(queryset, self.request, q)
        self.assertEqual(len(results_with_filtered_examples), 1)
        self.assertEqual(len(results_with_filtered_examples[0]['examples']), 1)

    def test_build_examples_from_queryset(self):
        artist_ = self.create_an_artist()
        song_ = self.create_a_song(artist_)
        self.create_an_example(song_, artist_)
        results = build_examples_from_queryset(Example.objects.all(), self.request)
        self.assertEqual(len(results), 1)

    def test_build_examples_from_annotations(self):
        artist_ = self.create_an_artist()
        sense_ = self.create_a_sense()
        song_ = self.create_a_song(artist_)
        example_ = self.create_an_example(song_, artist_)
        cat = Annotation(text="Cat", offset=example_.text.index("Cat"), example=example_, sense=sense_, owner=self.user)
        cat.save()
        results = build_examples_from_annotations(Annotation.objects.all(), self.request)
        self.assertEqual(len(results), 1)
