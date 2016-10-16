import random
import os


def check_for_image(slug, image_type='artists', folder='thumb'):
    jpg = 'website/static/website/img/{}/{}/{}.jpg'.format(image_type, folder, slug)
    png = 'website/static/website/img/{}/{}/{}.png'.format(image_type, folder, slug)
    images = []

    if os.path.isfile(jpg.encode('utf-8').strip()):
        images.append(jpg.replace('website/static/website/', '/static/website/'))
    if os.path.isfile(png.encode('utf-8').strip()):
        images.append(png.replace('website/static/website/', '/static/website/'))
    if len(images) == 0:
        return '/static/website/img/artists/{}/__none.png'.format(folder)
    else:
        return random.choice(images)


def reformat_name(name):
    if name.lower().endswith(', the'):
        return 'The ' + name[:-5]
    return name


def move_definite_article_to_end(name):
    if name.lower().startswith('the ') and len(name) > 4:
        return name[4:] + ' the'
    return name


def un_camel_case(name):
    n = name
    if n[0].islower():
        n = n[0].upper() + n[1:]
    tokens = re.findall('[A-Z][^A-Z]*', n)
    return ' '.join(tokens)


def build_annotation(annotation, a_type, rf=False):
    result = {
        "type": a_type,
        "annotation": annotation,
        "primary_artists": [build_artist(a) for a in annotation.song.primary_artist.order_by('name')],
        "featured_artists": [build_artist(a) for a in annotation.song.feat_artist.order_by('name')],
        "song_title": annotation.song.title,
        "song_slug": annotation.song.slug,
        "album": annotation.song.album,
        "release_date": str(annotation.song.release_date),
        "release_date_string": annotation.song.release_date_string,
    }
    return result


def build_artist(artist_object, require_origin=False):
    result = {
        "name": reformat_name(artist_object.name),
        "slug": artist_object.slug,
        "image": check_for_image(artist_object.slug, 'artists', 'thumb')
    }
    origin_results = artist_object.origin.all()
    if origin_results:
        origin_object = origin_results[0]
        if origin_object.longitude and origin_object.latitude:
            result['origin'] = {
                "name": origin_object.name,
                 "slug": origin_object.slug,
                 "longitude": origin_object.longitude,
                 "latitude": origin_object.latitude
            }

    if require_origin:
        if 'origin' in result:
            return result
        return None
    else:
        return result