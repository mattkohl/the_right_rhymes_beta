import re
# from api.serializers import ExampleHyperlinkedSerializer


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
    return "http://" + host + "/" + object_type + "/" + str(pk) + "/"


# def build_example_serializer(request, song, text):
#     host = request.get_host()
#     serializer_data = {
#         "text": text,
#         "artist": [make_uri(host, 'artists', artist.id) for artist in song.primary_artist.all()],
#         "feat_artist": [make_uri(host, 'artists', artist.id) for artist in song.feat_artist.all()],
#         "from_song": [make_uri(host, 'songs', song.id)]
#     }
#     example_serializer = ExampleHyperlinkedSerializer(context={'request': request}, data=serializer_data,
#                                                       partial=True)
#     example_serializer.is_valid()
#     return example_serializer


# def serialize_examples(request, song, q):
#     host = request.get_host()
#     serializers = []
#     lines = [line for line in song.lyrics.split('\n') if q in line]
#     for line in lines:
#         serializer_data = {
#             "text": line,
#             "artist": [make_uri(host, 'artists', artist.id) for artist in song.primary_artist.all()],
#             "feat_artist": [make_uri(host, 'artists', artist.id) for artist in song.feat_artist.all()],
#             "from_song": [make_uri(host, 'songs', song.id)]
#         }
#         example_serializer = ExampleHyperlinkedSerializer(context={'request': request}, data=serializer_data, partial=True)
#         example_serializer.is_valid()
#         serializers.append(example_serializer)
#
#     return serializers


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