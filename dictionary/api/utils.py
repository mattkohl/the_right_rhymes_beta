import re


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