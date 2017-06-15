import json
import requests

from django.core.management.base import BaseCommand, CommandError
import django.conf.global_settings as settings
from django.contrib.auth.models import User
from api.models import Sense, Artist, Song, Example, Place
from api.utils import clean_up_date


class Command(BaseCommand):

    def add_arguments(self, parser):
        parser.add_argument('--what',
                            default="sense",
                            help="What would you like to seed? (sense | song | artist | place)")

    def handle(self, *args, **options):
        owner = User.objects.first()
        if owner and owner.is_superuser:
            what = "sense"
            if 'what' in options:
                what = options['what']
            r = random_pipeline(owner, what)
            print(r)
            self.stdout.write(self.style.SUCCESS('Done!'))
        else:
            self.stdout.write(self.style.SUCCESS('Add a superuser first!'))


def get_random(what="sense"):
    urls = {
        "song": "https://www.therightrhymes.com/data/songs/random",
        "sense": "https://www.therightrhymes.com/data/senses/random",
        "place": "https://www.therightrhymes.com/data/places/random",
        "artist": "https://www.therightrhymes.com/data/artists/random",
        "example": "https://www.therightrhymes.com/data/examples/random",
    }

    if what in urls:
        url = urls[what]

        try:
            r = requests.get(url)
        except Exception as e:
            print(e)
        else:
            return json.loads(r.text)
    return None


def json_extract(result, owner, what="sense"):
    keys = {
        "sense": ('headword', 'part_of_speech', 'definition', 'notes', 'etymology'),
        "song": ('title', 'release_date', 'release_date_string', 'album'),
        "example": ('title', 'release_date', 'release_date_string', 'album', "text", "links"),
        "place": ('full_name', "longitude", "latitude"),
        "artist": ("name",)
    }

    s = dict((k, result[k]) for k in keys[what])

    if what == "song" or what == "example":
        add_keys = ("primary_artists", "featured_artists",)
        for key in add_keys:
            if key in result:
                s[key] = [persist("artist", {"name": o["name"], "owner": owner}) for o in result[key]]

    if what == "artist":
        key = "origin"
        if key in result:
            d = result[key]
            d.update({"owner": owner})
            s[key] = persist("place", d)
    s.update({"owner": owner})
    return s


def persist(what, data_dict):
    if what == 'sense':
        obj, created = Sense.objects.get_or_create(**data_dict)
    elif what == 'artist':
        obj, created = Artist.objects.get_or_create(**data_dict)
    elif what == 'place':
        obj, created = Place.objects.get_or_create(**data_dict)
    elif what == 'song':
        featured_artists, primary_artists, data_dict = extract_artists(data_dict)
        obj = create_a_song(data_dict, featured_artists, primary_artists)
    elif what == 'example':
        featured_artists, primary_artists, data_dict = extract_artists(data_dict)
        obj = create_an_example(data_dict, featured_artists, primary_artists)
    else:
        obj = None
        print("Failed to persist", what, ": ", str(data_dict))
    return obj


def create_an_example(data_dict, featured_artists, primary_artists):
    text = data_dict.pop("text")
    links = data_dict.pop("links")
    song = create_a_song(data_dict, featured_artists, primary_artists)
    obj, created = Example.objects.get_or_create(text=text, from_song=song, owner=data_dict["owner"])
    obj.primary_artists.add(*primary_artists)
    obj.featured_artists.add(*featured_artists)
    return obj


def create_a_song(data_dict, featured_artists, primary_artists):
    obj, created = Song.objects.get_or_create(**data_dict)
    obj.primary_artists.add(*primary_artists)
    obj.featured_artists.add(*featured_artists)
    return obj


def extract_artists(data_dict):
    PA = "primary_artists"
    FA = "featured_artists"
    primary_artists, featured_artists = [], []
    if PA in data_dict:
        primary_artists = data_dict.pop(PA)
    if FA in data_dict:
        featured_artists = data_dict.pop(FA)
    return featured_artists, primary_artists, data_dict



test_example = {
        "album": "Tha Absolute Truth",
        "text": "Big Tuck in the building, the chillest nigga in town",
        "featured_artists": [
            {
                "image": "/static/dictionary/img/artists/thumb/__none.png",
                "name": "Dre",
                "slug": "dre"
            }
        ],
        "primary_artists": [
            {
                "image": "/static/dictionary/img/artists/thumb/big-tuck.jpg",
                "name": "Big Tuck",
                "origin": {
                    "latitude": 32.776272,
                    "name": "Dallas",
                    "slug": "dallas-texas-usa",
                    "longitude": -96.796856
                },
                "slug": "big-tuck"
            }
        ],
        "title": "That What's Up",
        "release_date": "2006-12-12",
        "links": [
            {
                "offset": 0,
                "target_lemma": "Big Tuck",
                "type": "artist",
                "target_slug": "big-tuck",
                "text": "Big Tuck"
            },
            {
                "offset": 30,
                "target_lemma": "chill",
                "type": "xref",
                "target_slug": "chill#e4000_adj_1",
                "text": "chillest"
            }
        ],
        "release_date_string": "2006-12-12"
    }


def random_pipeline(owner, what):
    random_json = get_random(what)
    if random_json:
        data_dict = json_extract(random_json, owner, what)
        persisted = persist(what, data_dict)
        return persisted
    return None
