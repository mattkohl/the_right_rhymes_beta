import re
from api.serializers import AnnotationSerializer, ExampleSerializer
from api.models import Sense, Place, Artist


def extract_rhymes(annotations):
    rhyme_set = set()
    for a in annotations:
        for r in a.rhymes.all():
            rhyme_set.add((r, a))
    rhymes = []
    for rhyme in rhyme_set:
        rhymes.append({
            'left': rhyme[0],
            'right': rhyme[1]
        })
    return rhymes


def make_uri(host, object_type, pk):
    uri = "http://" + host + "/" + object_type + "/" + str(pk) + "/"
    return uri


def build_annotation_serializer(request, example, text="", offset=None):
    host = request.get_host()
    serializer_data = {
        "text": text,
        "offset": offset,
        "example": make_uri(host, 'examples', example.id)
    }
    annotation_serializer = AnnotationSerializer(context={'request': request}, data=serializer_data, partial=True)
    annotation_serializer.is_valid()
    return annotation_serializer


def build_example_serializer(request, song, text):
    host = request.get_host()
    serializer_data = {
        "text": text,
        "primary_artists": [make_uri(host, 'artists', artist.id) for artist in song.primary_artists.all()],
        "featured_artists": [make_uri(host, 'artists', artist.id) for artist in song.featured_artists.all()],
        "from_song": make_uri(host, 'songs', song.id)
    }
    example_serializer = ExampleSerializer(context={'request': request}, data=serializer_data,
                                           partial=True)
    example_serializer.is_valid()
    return example_serializer


def serialize_examples(request, song, q):
    host = request.get_host()
    serializers = []
    lines = [line for line in song.lyrics.split('\n') if q in line]
    for line in lines:
        serializer_data = {
            "text": line,
            "primary_artists": [make_uri(host, 'artists', artist.id) for artist in song.primary_artists.all()],
            "featured_artists": [make_uri(host, 'artists', artist.id) for artist in song.featured_artists.all()],
            "from_song": make_uri(host, 'songs', song.id)
        }
        example_serializer = ExampleSerializer(context={'request': request}, data=serializer_data, partial=True)
        example_serializer.is_valid()
        serializers.append(example_serializer)

    return serializers


def slugify(text):
    slug = text.strip().lower()
    if slug[0] == "'" or slug[0] == "-":
        slug = slug[1:]
    slug = re.sub("[\s.]", "-", slug)
    slug = re.sub("\$", "s", slug)
    slug = re.sub("%", "percent", slug)
    slug = re.sub("&amp;", "and", slug)
    slug = re.sub("&", "and", slug)
    slug = re.sub("\+", "and", slug)
    slug = re.sub("@", "at", slug)
    slug = re.sub("½", "half", slug)
    from django.utils.text import slugify
    return slugify(slug)


def clean_up_date(unformatted_date):
    new_date = unformatted_date
    month = new_date[-2:]
    if len(new_date) == 7 and month == '02':
        return new_date + '-28'
    if len(new_date) == 7 and month in ['04', '06', '11', '09']:
        return new_date + '-30'
    if len(new_date) == 7:
        return new_date + '-31'
    if len(new_date) == 4:
        return new_date + '-12-31'
    return new_date


def clean_text(text):
    t1 = text.replace("’", "'")
    return t1


def render_example_with_annotations(request, example):
    host = request.get_host()
    buffer = 0
    rendered = example.text
    for annotation in example.annotations.order_by('offset'):
        link = build_annotation_link(host, annotation)
        start = buffer + annotation.offset
        end = start + len(annotation.text)
        rendered = rendered[:start] + link + rendered[end:]
        buffer += len(link) - len(annotation.text)
    return rendered


def build_annotation_link(host, annotation):
    link = '<a href="{}">{}</a>'
    uri = "#"
    target = annotation.get_link()
    if target:
        if isinstance(target, Sense):
            uri = make_uri(host, "senses", target.id)
        if isinstance(target, Artist):
            uri = make_uri(host, "artists", target.id)
        if isinstance(target, Place):
            uri = make_uri(host, "places", target.id)
        return link.format(uri, annotation.text)
    return "<span>{}</span>".format(annotation.text)


def build_examples_from_annotations(annotations, request):
    return [
        {
            "id": a.example.id,
            "text": a.example.text,
            "rendered": render_example_with_annotations(request, a.example),
            "song": a.example.from_song,
            'annotations': a.example.annotations.all(),
            "primary_artists": a.example.from_song.primary_artists.all(),
            "featured_artists": a.example.from_song.featured_artists.first(),
        } for a in annotations]


def build_examples_from_queryset(queryset, request):
    return [
        {
            'id': example.id,
            'text': example.text,
            "rendered": render_example_with_annotations(request, example),
            'song': example.from_song,
            'annotations': example.annotations.all(),
            'primary_artists': example.primary_artists.all(),
            'featured_artists': example.featured_artists.all(),
        } for example in queryset]


def build_songs_from_queryset(queryset, request, example_filter):
    return [
        {
            "id": song.id,
            "release_date": song.release_date,
            "title": song.title,
            "album": song.album,
            "primary_artists": song.primary_artists.all(),
            "featured_artists": song.featured_artists.all(),
            "examples": build_examples_from_queryset(song.examples.filter(text__icontains=example_filter), request) if example_filter is not None else []
        } for song in queryset]
