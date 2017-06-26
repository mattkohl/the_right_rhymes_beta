from rest_framework import serializers
from django.contrib.auth.models import User
from api.models import Sense, Artist, Place, Song, Domain, SemanticClass, Annotation, Dictionary, Example


class SenseSerializer(serializers.HyperlinkedModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.username')
    highlight = serializers.HyperlinkedIdentityField(view_name='sense-highlight', format='html')

    class Meta:
        model = Sense
        fields = (
            'url',
            'highlight',
            'headword',
            'published',
            'part_of_speech',
            'definition',
            'etymology',
            'notes',
            'domains',
            'semantic_classes',
            'derivatives',
            'derives_from',
            'synonyms',
            'antonyms',
            'hypernyms',
            'hyponyms',
            'holonyms',
            'meronyms',
            'annotations',
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
            'also_known_as',
            'members',
            'origin',
            'primary_songs',
            'featured_songs',
            'annotations',
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
            'full_name',
            'latitude',
            'longitude',
            'artists',
            'contains',
            'within',
            'annotations',
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
            'release_date_string',
            'title',
            'album',
            'lyrics',
            'primary_artists',
            'featured_artists',
            'examples',
            'release_date_verified',
            'owner'
        )


class DictionarySerializer(serializers.HyperlinkedModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.username')
    highlight = serializers.HyperlinkedIdentityField(view_name='dictionary-highlight', format='html')

    class Meta:
        model = Dictionary
        fields = (
            'url',
            'name',
            'highlight',
            'senses',
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
            'highlight',
            'broader',
            'narrower',
            'senses',
            'owner'
        )


class SemanticClassSerializer(serializers.HyperlinkedModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.username')
    highlight = serializers.HyperlinkedIdentityField(view_name='semanticclass-highlight', format='html')

    class Meta:
        model = SemanticClass
        fields = (
            'url',
            'name',
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
            'text',
            'highlight',
            'from_song',
            'primary_artists',
            'featured_artists',
            'annotations',
            'owner'
        )


class AnnotationSerializer(serializers.HyperlinkedModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.username')
    highlight = serializers.HyperlinkedIdentityField(view_name='annotation-highlight', format='html')

    class Meta:
        model = Annotation
        fields = (
            'url',
            'text',
            'highlight',
            'example',
            'offset',
            'rhymes',
            'sense',
            'artist',
            'place',
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

