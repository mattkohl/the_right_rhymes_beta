import copy
import responses

from api.tests.test_models import BaseTest
from api.models import Sense, Artist, Song, Example, Place
from api.management.commands.seed_database import extract_dict, persist, get_random_thing, random_pipeline, \
    inject_owner, remove_image, process_origin, extract_and_process_artists


null = None


class SeedDatabaseTest(BaseTest):

    @responses.activate
    def test_get_random_thing(self):
        responses.add(responses.GET, "https://www.therightrhymes.com/data/senses/random",
                      body='{"definition": "test definition"}', status=202,
                      content_type='application/json')

        r = get_random_thing()
        self.assertTrue("definition" in r)
        self.assertEqual(r["definition"], "test definition")

    @responses.activate
    def test_random_pipeline(self):
        responses.add(responses.GET, "https://www.therightrhymes.com/data/senses/random",
                      body="""
                        {
                            "headword": "test headword", 
                            "definition": "test definition", 
                            "part_of_speech": "noun", 
                            "notes": "test notes", 
                            "etymology": "test etym"
                        }
                        """,
                      status=202,
                      content_type='application/json')
        r = random_pipeline(self.user, "sense")
        self.assertIsInstance(r, Sense)

    def test_random_pipeline_bad_input(self):
        r = random_pipeline(self.user, "blah")
        self.assertTrue(r is None)

    def test_inject_owner(self):
        data = {
            "a": "a",
            "b": {"c": "c"},
            "d": [
                {"e": "e"},
                {"f": "f"},
            ],
        }
        injected = {
            'a': 'a',
            'b': {'c': 'c', 'owner': 'user'},
            'd': [
                {'e': 'e', 'owner': 'user'},
                {'f': 'f', 'owner': 'user'}
            ],
            'owner': 'user'
        }

        inject_owner("user", data)
        self.assertEqual(data, injected)


class SeedDatabaseSenseTest(BaseTest):

    result = {
        "form": null,
        "antonyms": [],
        "holonyms": [],
        "artist_name": "Main Source",
        "part_of_speech": "adverb",
        "semantic_classes": [
            {
                "slug": "accolades",
                "name": "Accolades"
            }
        ],
        "ancestors": [],
        "domains": [],
        "derivatives": [],
        "definition": "appropriately, to a suitable degree",
        "related_words": [],
        "instances": [],
        "image": "/static/dictionary/img/artists/full/main-source.jpg",
        "num_examples": 29,
        "collocates": [
            {
                "frequency": 3,
                "collocate_lemma": "break off",
                "target_id": "e3420_trPhrV_2",
                "target_slug": "break-off",
                "source_sense_xml_id": "e8680_adv_1"
            }
        ],
        "rhymes": [
            {
                "rhyme_slug": "hip-hoppers",
                "parent_sense_xml_id": "e8680_adv_1",
                "rhyme": "hip-hoppers",
                "frequency": 2
            }
        ],
        "headword": "proper",
        "related_concepts": [
            {
                "target_id": "e8690_n_1",
                "target_slug": "props",
                "xref_type": "Related Concept",
                "target_lemma": "props",
                "xref_word": "props"
            }
        ],
        "etymology": "",
        "sense_image": null,
        "regions": [],
        "notes": "",
        "examples": [
            {
                "release_date_string": "1991-07-23",
                "release_date": "1991-07-23",
                "album": "Breaking Atoms",
                "lyric": "They speak proper while my speech is from a garbage can",
                "artist_name": "Main Source",
                "artist_slug": "main-source",
                "song_slug": "main-source-lookin-at-the-front-door",
                "song_title": "Lookin At The Front Door",
                "featured_artists": [],
                "linked_lyric": "They speak <a href=\"/proper#e8680_adv_1\">proper</a> while my speech is from a garbage can"
            }
        ],
        "instance_of": [],
        "artist_slug": "main-source",
        "meronyms": [],
        "synonyms": [],
        "xml_id": "e8680_adv_1"
    }

    def test_extract_dict(self):

        extracted = extract_dict(self.result, self.user, "sense")
        self.assertTrue("owner" in extracted)
        self.assertEqual(extracted['owner'], self.user)

    def test_persist(self):

        extracted = extract_dict(self.result, self.user, "sense")
        persisted = persist("sense", extracted)
        self.assertIsInstance(persisted, Sense)


class SeedDatabaseArtistTest(BaseTest):

    result = {
        "slug": "kurtis-blow",
        "image": "/static/dictionary/img/artists/thumb/kurtis-blow.png",
        "name": "Kurtis Blow",
        "origin": {
            "longitude": -73.986581,
            "slug": "new-york-city-new-york-usa",
            "latitude": 40.730599,
            "name": "New York City"
        }
    }

    def test_extract_dict(self):

        extracted = extract_dict(self.result, self.user, "artist")
        self.assertTrue("owner" in extracted)
        self.assertEqual(extracted['owner'], self.user)
        self.assertTrue("origin" in extracted)

    def test_persist(self):

        extracted = extract_dict(self.result, self.user, "artist")
        persisted = persist("artist", extracted)
        self.assertIsInstance(persisted, Artist)
        self.assertIsInstance(persisted.origin, Place)

    def test_artist_with_and_without_origin_persist(self):

        without_origin = copy.deepcopy(self.result)
        without_origin.pop("origin")
        self.assertTrue("origin" not in without_origin)
        without_extracted = extract_dict(self.result, self.user, "artist")
        persist("artist", without_extracted)

        with_extracted = extract_dict(self.result, self.user, "artist")
        persist("artist", with_extracted)

        self.assertTrue(Artist.objects.count(), 1)
        self.assertEqual(Artist.objects.first().name, "Kurtis Blow")

    def test_remove_image(self):
        self.assertTrue("image" in self.result)
        remove_image(self.result)
        self.assertTrue("image" not in self.result)

    def test_process_origin(self):
        self.assertTrue("origin" in self.result)
        self.assertIsInstance(self.result["origin"], dict)
        process_origin(self.result)
        self.assertIsInstance(self.result["origin"], Place)

    def test_extract_and_process_artists(self):
        extracted = extract_dict(self.result, self.user, "artist")
        data = {"primary_artists": [extracted]}
        featured_artists, primary_artists, data_dict = extract_and_process_artists(data)
        self.assertTrue("primary_artists" not in data_dict)
        self.assertEqual(len(primary_artists), 1)
        self.assertIsInstance(primary_artists[0], Artist)


class SeedDatabaseSongTest(BaseTest):

    result = {
        "release_date_string": "1994-09-27",
        "album": "Shade Business",
        "primary_artists": [
            {
                "slug": "pmd",
                "image": "/static/dictionary/img/artists/thumb/pmd.jpg",
                "name": "PMD",
                "origin": {
                    "longitude": -73.179329,
                    "slug": "smithtown-long-island-new-york-usa",
                    "latitude": 40.807337,
                    "name": "Smithtown"
                }
            }
        ],
        "featured_artists": [
            {
                "slug": "zone-7",
                "image": "/static/dictionary/img/artists/thumb/__none.png",
                "name": "Zone 7"
            }
        ],
        "release_date": "1994-09-27",
        "slug": "pmd-ill-wait",
        "title": "I'll Wait"
    }

    def test_extract_dict(self):
        extracted = extract_dict(self.result, self.user, "song")
        self.assertTrue("owner" in extracted)
        self.assertEqual(extracted['owner'], self.user)

    def test_persist(self):
        extracted = extract_dict(self.result, self.user, "song")
        persisted = persist("song", extracted)
        self.assertIsInstance(persisted, Song)


class SeedDatabaseExampleTest(BaseTest):

    result = {
        "links": [
            {
                "offset": 10,
                "target_lemma": "gaffle",
                "type": "xref",
                "target_slug": "gaffle#e5593_trV_2",
                "text": "gaffle"
            },
            {
                "offset": 21,
                "target_lemma": "scratch",
                "type": "xref",
                "target_slug": "scratch#e9290_n_1",
                "text": "scratch"
            },
            {
                "offset": 32,
                "target_lemma": "gat",
                "type": "xref",
                "target_slug": "gat#e5680_n_1",
                "text": "gat"
            }
        ],
        "title": "Kill Street Blues",
        "text": "Tryin' to gaffle the scratch my gat consumes",
        "featured_artists": [],
        "release_date_string": "1997-10-28",
        "release_date": "1997-10-28",
        "album": "The Black Bossalini",
        "primary_artists": [
            {
                "origin": {
                    "slug": "hayward-california-usa",
                    "name": "Hayward",
                    "latitude": 37.668821,
                    "longitude": -122.080796
                },
                "slug": "spice-1",
                "name": "Spice 1",
                "image": "/static/dictionary/img/artists/thumb/spice-1.png"
            }
        ]
    }

    def test_extract_dict(self):
        extracted = extract_dict(self.result, self.user, "example")
        self.assertTrue("owner" in extracted)
        self.assertEqual(extracted['owner'], self.user)

    def test_persist(self):
        extracted = extract_dict(self.result, self.user, "example")
        persisted = persist("example", extracted)
        self.assertIsInstance(persisted, Example)
        self.assertEqual(persisted.primary_artists.count(), 1)
        [self.assertIsInstance(a, Artist) for a in persisted.primary_artists.all()]
        self.assertEqual(Song.objects.count(), 1)
        self.assertIsInstance(persisted.from_song, Song)

