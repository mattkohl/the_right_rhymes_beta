from django.conf.urls import url
from django.contrib import admin
# from django.contrib.sitemaps.views import sitemap
from . import views
# from dictionary.sitemaps import EntrySitemap, ArtistSitemap, SongSitemap
#
# sitemaps = {
#     'entries': EntrySitemap,
#     'artists': ArtistSitemap,
#     'songs': SongSitemap
# }


urlpatterns = [

    # /annotations/<annotation-slug>/
    url(r"^annotations/(?P<annotation_slug>[a-zA-Z0-9\-_'’,\(\)\+\!\*ōé½@áó]+)/$", views.annotation, name='annotation'),

    # /artists/<artist-slug>/
    url(r"^artists/(?P<artist_slug>[a-zA-Z0-9\-_'’,\(\)\+\!\*ōé½@áó]+)/$", views.artist, name='artist'),

]