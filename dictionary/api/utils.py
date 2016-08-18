import re


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