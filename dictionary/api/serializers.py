from rest_framework import serializers
from django.contrib.auth.models import User
from api.models import Sense, Artist, Place, Song


class SenseSerializer(serializers.HyperlinkedModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.username')
    highlight = serializers.HyperlinkedIdentityField(view_name='sense-highlight', format='html')

    class Meta:
        model = Sense
        fields = (
            'url',
            'highlight',
            'headword',
            'headword_slug',
            'published',
            'part_of_speech',
            'definition',
            'etymology',
            'notes',
            'synonyms',
            'antonyms',
            'hypernyms',
            'hyponyms',
            'holonyms',
            'meronyms',
            'owner'
        )


class ArtistSerializer(serializers.HyperlinkedModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.username')
    highlight = serializers.HyperlinkedIdentityField(view_name='artist-highlight', format='html')

    class Meta:
        model = Artist
        fields = (
            'url',
            'highlight',
            'name',
            'slug',
            'also_known_as',
            'members',
            'origin',
            'primary_songs',
            'featured_songs',
            'owner'
        )


class PlaceSerializer(serializers.HyperlinkedModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.username')
    highlight = serializers.HyperlinkedIdentityField(view_name='place-highlight', format='html')

    class Meta:
        model = Place
        fields = (
            'url',
            'highlight',
            'name',
            'full_name',
            'slug',
            'longitude',
            'latitude',
            'artists',
            'contains',
            'within',
            'owner'
        )


class SongSerializer(serializers.HyperlinkedModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.username')
    highlight = serializers.HyperlinkedIdentityField(view_name='song-highlight', format='html')

    class Meta:
        model = Song
        fields = (
            'url',
            'highlight',
            'slug',
            'release_date_string',
            'release_date',
            'title',
            'album',
            'lyrics',
            'primary_artist',
            'feat_artist',
            'release_date_verified',
            'owner'
        )


class UserSerializer(serializers.HyperlinkedModelSerializer):
    senses = serializers.HyperlinkedRelatedField(many=True, view_name='sense-detail', read_only=True)

    class Meta:
        model = User
        fields = (
            'url',
            'username',
            'artists',
            'places',
            'senses',
            'songs',
        )

