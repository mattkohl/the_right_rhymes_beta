from django.contrib import admin

from api.models import Sense, Artist, Song, Place, Domain, SemanticClass


@admin.register(Artist)
class ArtistAdmin(admin.ModelAdmin):
    list_display = ['name']


@admin.register(Domain)
class DomainAdmin(admin.ModelAdmin):
    list_display = ['name']


@admin.register(Place)
class PlaceAdmin(admin.ModelAdmin):
    list_display = ['name', 'full_name', 'slug']


@admin.register(SemanticClass)
class SemanticClassAdmin(admin.ModelAdmin):
    list_display = ['name']


@admin.register(Sense)
class SenseAdmin(admin.ModelAdmin):
    list_display = ['headword', 'part_of_speech', 'definition']


@admin.register(Song)
class SongAdmin(admin.ModelAdmin):
    list_display = ['title', 'album', 'release_date']
