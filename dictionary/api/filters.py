import django_filters
from api.models import Artist, Song, Example, Place, Sense
from rest_framework import filters


class ArtistFilter(filters.FilterSet):
    name = django_filters.CharFilter(lookup_expr='icontains')

    class Meta:
        model = Artist
        fields = []


class PlaceFilter(filters.FilterSet):
    name = django_filters.CharFilter(lookup_expr='icontains')
    full_name = django_filters.CharFilter(lookup_expr='icontains')
    artists = django_filters.CharFilter(name="artists__name", lookup_expr='icontains', )

    class Meta:
        model = Place
        fields = []


class ExampleFilter(filters.FilterSet):
    text = django_filters.CharFilter(lookup_expr='icontains')
    primary_artist_name = django_filters.CharFilter(name="primary_artist__name", lookup_expr='icontains', )

    class Meta:
        model = Example
        fields = []


class SenseFilter(filters.FilterSet):
    headword = django_filters.CharFilter(lookup_expr='icontains')
    definition = django_filters.CharFilter(lookup_expr='icontains')
    part_of_speech = django_filters.CharFilter(lookup_expr='icontains')

    class Meta:
        model = Sense
        fields = []


class SongFilter(filters.FilterSet):
    lyrics = django_filters.CharFilter(lookup_expr='icontains')
    release_date_string = django_filters.CharFilter(lookup_expr='icontains')
    primary_artist_name = django_filters.CharFilter(name="primary_artist__name", lookup_expr='icontains', )
    featured_artist_name = django_filters.CharFilter(name="feat_artist__name", lookup_expr='icontains', )

    class Meta:
        model = Song
        fields = ['album', 'release_date']


