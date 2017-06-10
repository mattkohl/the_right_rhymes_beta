import json
import requests

from django.core.management.base import BaseCommand, CommandError
import django.conf.global_settings as settings
from django.contrib.auth.models import User
from api.models import Sense, Artist, Song, Example, Place
from api.utils import make_uri


class Command(BaseCommand):

    def handle(self, *args, **options):
        owner = User.objects.first()
        if owner:
            # r = random_sense_pipeline(owner)
            r = random_pipeline(owner, "song")
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

    url = urls[what]

    try:
        r = requests.get(url)
    except Exception as e:
        print(e)
    else:
        return json.loads(r.text)


def json_extract(result, owner, what="sense"):
    keys = {
        "sense": ('headword', 'part_of_speech', 'definition'),
        "song": ('title', 'release_date_string', 'album'),
        "place": ('full_name', "longitude", "latitude"),
        "artist": ("name",)
    }

    s = dict((k, result[k]) for k in keys[what])

    if what == "song":
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
        PA = "primary_artists"
        FA = "featured_artists"
        data_dict["release_date"] = data_dict.pop("release_date_string")
        primary_artists, featured_artists = [], []
        if PA in data_dict:
            primary_artists = data_dict.pop(PA)
        if FA in data_dict:
            featured_artists = data_dict.pop(FA)
        obj, created = Song.objects.get_or_create(**data_dict)
        obj.primary_artists.add(*primary_artists)
        obj.featured_artists.add(*featured_artists)
    elif what == 'example':
        obj, created = Example.objects.get_or_create(**data_dict)
    else:
        obj = None
        print("Failed to persist", what, ": ", str(data_dict))
    return obj


def random_pipeline(owner, what):
    random_json = get_random(what)
    if random_json:
        data_dict = json_extract(random_json, owner, what)
        persisted = persist(what, data_dict)
        return persisted
    return None
