import re
from api.serializers import AnnotationSerializer


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
    uri = "http://" + host + "/data/" + object_type + "/" + str(pk) + "/"
    print(uri)
    return uri


def build_annotation_serializer(request, song, text="", context="", start_position=None, end_position=None):
    host = request.get_host()
    serializer_data = {
        "text": text,
        "context": context,
        "start_position": start_position,
        "end_position": end_position,
        "song": make_uri(host, 'songs', song.id)
    }
    annotation_serializer = AnnotationSerializer(context={'request': request}, data=serializer_data, partial=True)
    annotation_serializer.is_valid()
    return annotation_serializer


def serialize_annotations(request, song, q):
    lines = list(set([line for line in song.lyrics.split('\n') if q.lower() in line.lower()]))
    return [build_annotation_serializer(request, song, line, q, line.index(q), line.index(q) + len(q)) for line in lines]


def slugify(text):
    slug = text.strip().lower()
    if slug[0] == "'" or slug[0] == "-":
        slug = slug[1:]
    slug = re.sub("^[\-']]", "", slug)
    slug = re.sub("[\s\.]", "-", slug)
    slug = re.sub("[:/]", "", slug)
    slug = re.sub("\$", "s", slug)
    slug = re.sub("\*", "", slug)
    slug = re.sub("#", "number", slug)
    slug = re.sub("%", "percent", slug)
    slug = re.sub("&amp;", "and", slug)
    slug = re.sub("&", "and", slug)
    slug = re.sub("\+", "and", slug)

    slug = re.sub("é", "e", slug)
    slug = re.sub("ó", "o", slug)
    slug = re.sub("á", "a", slug)
    slug = re.sub("@", "at", slug)
    slug = re.sub("½", "half", slug)
    slug = re.sub("ō", "o", slug)

    slug = re.sub("'", "", slug)
    slug = re.sub(",", "", slug)
    slug = re.sub("-$", "", slug)
    slug = re.sub("\?", "", slug)
    slug = re.sub("[\(\)]", "", slug)
    return slug