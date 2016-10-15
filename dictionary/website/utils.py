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