import json
import requests

from django.core.management.base import BaseCommand, CommandError
import django.conf.global_settings as settings
from django.contrib.auth.models import User
from api.models import Sense, Artist, Song, Example, Annotation


class Command(BaseCommand):

    def handle(self, *args, **options):
        owner = User.objects.first()
        if owner:
            r = random_sense_pipeline(owner)
            print(r)
            self.stdout.write(self.style.SUCCESS('Done!'))
        else:
            self.stdout.write(self.style.SUCCESS('Add a superuser first!'))


def get_random(what="sense"):
    if what == 'sense':
        url = "http://www.therightrhymes.com/data/senses/random"
    else:
        url = "http://www.therightrhymes.com/data/entries/random"
    try:
        r = requests.get(url)
    except Exception as e:
        print(e)
    else:
        return json.loads(r.text)


def json_extract(result, owner):
    s = dict((k, result[k]) for k in ('headword', 'part_of_speech', 'definition'))
    s.update({"owner": owner})
    return s


def persist(what, data_dict):
    if what == 'sense':
        obj, created = Sense.objects.get_or_create(**data_dict)
    elif what == 'artist':
        obj, created = Artist.objects.get_or_create(**data_dict)
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


