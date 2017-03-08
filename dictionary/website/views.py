import json
import logging
from operator import itemgetter

from django.db.models import Q, Count
from django.db.models.functions import Lower
from django.http import HttpResponse
from django.shortcuts import redirect, get_object_or_404, get_list_or_404
from django.template import loader
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_http_methods
from django.views.decorators.cache import cache_control

from website.utils import check_for_image, build_annotation
from api.models import Sense, Artist, Domain, Place, Song, SemanticClass, Annotation
from api.utils import slugify

logger = logging.getLogger(__name__)
NUM_QUOTS_TO_SHOW = 3
NUM_ARTISTS_TO_SHOW = 6


def annotation(request, annotation_slug):
    annotation_results = get_list_or_404(Annotation, slug=annotation_slug)

    template = loader.get_template('website/annotation.html')
    context = {
        "annotations": [annotation for annotation in annotation_results]
    }
    return HttpResponse(template.render(context, request))


def artist(request, artist_slug):
    artist_results = get_list_or_404(Artist, slug=artist_slug)
    artist = artist_results[0]
    origin_results = artist.origin.all()
    if origin_results:
        origin = origin_results[0].full_name
        origin_slug = origin_results[0].slug
        long = origin_results[0].longitude
        lat = origin_results[0].latitude
    else:
        origin = ''
        origin_slug = ''
        long = ''
        lat = ''

    primary_songs = artist.primary_songs.all()
    featured_songs = artist.featured_songs.all()

    print(list(primary_songs))
    print(list(featured_songs))
    artist_annotations = [build_annotation(a, 'artist') for a in artist.annotations.all()]
    image = check_for_image(artist.slug, 'artists', 'full')
    thumb = check_for_image(artist.slug, 'artists', 'thumb')

    template = loader.get_template('website/artist.html')

    context = {
        'artist': artist.name,
        'slug': artist.slug,
        'origin': origin,
        'origin_slug': origin_slug,
        'longitude': long,
        'latitude': lat,
        'artist_annotations': artist_annotations,
        'artist_annotation_count': len(artist_annotations),
        'entity_examples': [],
        'entity_example_count': 0,
        'image': image,
        'thumb': thumb,
        'also_known_as': [{
            'artist': aka.name,
            'slug': aka.slug
        } for aka in artist.also_known_as.all()]
    }
    return HttpResponse(template.render(context, request))


def entry(request, headword_slug):
    if '#' in headword_slug:
        slug = headword_slug.split('#')[0]
    else:
        slug = headword_slug
    template = loader.get_template('website/entry.html')

    senses = Sense.objects.filter(headword=slug)
    if senses:
        headword = senses.first().headword
        context = {
            'headword': headword,
            'slug': headword_slug,
            'title': headword[0].upper() + headword[1:],
            'image': "",
            'pub_date': "",
            'last_updated': "",
            'senses': [s.to_dict() for s in senses],
            'published_entries': []
        }
        import pprint
        pprint.pprint(context)
        return HttpResponse(template.render(context, request))