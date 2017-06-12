import copy

from api.tests.test_models import BaseTest
from api.models import Sense, Artist, Song, Example, Place
from api.management.commands.seed_database import json_extract, persist, get_random, random_pipeline


null = None


class SeedDatabaseTest(BaseTest):

    def test_get_random(self):
        r = get_random()
        self.assertTrue("definition" in r)

    def test_random_pipeline(self):
        r = random_pipeline(self.user, "song")
        self.assertTrue(isinstance(r, Song))

    def test_random_pipeline_bad_input(self):
        r = random_pipeline(self.user, "blah")
        self.assertTrue(r is None)


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

    def test_sense_json_extract(self):

        extracted = json_extract(self.result, self.user, "sense")
        self.assertTrue("owner" in extracted)
        self.assertEqual(extracted['owner'], self.user)

    def test_sense_persist(self):

        extracted = json_extract(self.result, self.user, "sense")
        persisted = persist("sense", extracted)
        self.assertTrue(isinstance(persisted, Sense))


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

    def test_artist_json_extract(self):

        extracted = json_extract(self.result, self.user, "artist")
        self.assertTrue("owner" in extracted)
        self.assertEqual(extracted['owner'], self.user)
        self.assertTrue(isinstance(extracted['origin'], Place))

    def test_artist_persist(self):

        extracted = json_extract(self.result, self.user, "artist")
        persisted = persist("artist", extracted)
        self.assertTrue(isinstance(persisted, Artist))

    def test_artist_with_and_without_origin_persist(self):

        without_origin = copy.deepcopy(self.result)
        without_origin.pop("origin")
        self.assertTrue("origin" not in without_origin)
        without_extracted = json_extract(self.result, self.user, "artist")
        persist("artist", without_extracted)

        with_extracted = json_extract(self.result, self.user, "artist")
        persist("artist", with_extracted)

        self.assertTrue(Artist.objects.count(), 1)
        self.assertEqual(Artist.objects.first().name, "Kurtis Blow")


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

    def test_song_json_extract(self):

        extracted = json_extract(self.result, self.user, "song")
        self.assertTrue("owner" in extracted)
        self.assertEqual(extracted['owner'], self.user)

    def test_song_persist(self):
        extracted = json_extract(self.result, self.user, "song")
        persisted = persist("song", extracted)
        self.assertTrue(isinstance(persisted, Song))
