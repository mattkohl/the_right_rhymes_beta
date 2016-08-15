from rest_framework import serializers
from django.contrib.auth.models import User
from api.models import Sense, Artist, Place, Song, Domain, SemanticClass, Example


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


class DomainSerializer(serializers.HyperlinkedModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.username')
    highlight = serializers.HyperlinkedIdentityField(view_name='domain-highlight', format='html')

    class Meta:
        model = Domain
        fields = (
            'url',
            'name',
            'slug',
            'highlight',
            'broader',
            'narrower',
            'senses',
            'owner'
        )


class SemanticClassSerializer(serializers.HyperlinkedModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.username')
    highlight = serializers.HyperlinkedIdentityField(view_name='semantic-class-highlight', format='html')

    class Meta:
        model = SemanticClass
        fields = (
            'url',
            'name',
            'slug',
            'highlight',
            'broader',
            'narrower',
            'senses',
            'owner'
        )


class ExampleSerializer(serializers.HyperlinkedModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.username')
    highlight = serializers.HyperlinkedIdentityField(view_name='example-highlight', format='html')

    class Meta:
        model = Example
        fields = (
            'url',
            'slug',
            'text',
            'highlight',
            'from_song',
            'artist',
            'feat_artist',
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

