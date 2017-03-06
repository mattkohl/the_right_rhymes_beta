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
            sense_json = get_random()
            if sense_json:
                data_dict = dict((k, sense_json[k]) for k in ('headword', 'part_of_speech', 'definition'))
                data_dict.update({"owner": owner})
                persisted = persist("sense", data_dict)
                print(persisted)
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


