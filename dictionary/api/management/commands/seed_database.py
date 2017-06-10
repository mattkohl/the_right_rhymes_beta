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
            r = random_pipeline(owner, "artist")
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
                # TODO: still doesn't work!
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
        obj, created = Song.objects.get_or_create(**data_dict)
    elif what == 'example':
        obj, created = Example.objects.get_or_create(**data_dict)
    else:
        obj = None
        print("Failed to persist", what, ": ", str(data_dict))
    return obj


def random_sense_pipeline(owner):
    random_sense_json = get_random()
    if random_sense_json:
        data_dict = json_extract(random_sense_json, owner)
        persisted = persist("sense", data_dict)
        return persisted
    return None


def random_pipeline(owner, what):
    random_json = get_random(what)
    if random_json:
        data_dict = json_extract(random_json, owner, what)
        persisted = persist(what, data_dict)
        return persisted
    return None


def one_of_everything(owner):
    sense = get_random("sense")
    place = get_random("place")
    artist = get_random("artist")
    song = get_random("song")
