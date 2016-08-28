from rest_framework import permissions, renderers, viewsets, filters
from rest_framework.response import Response
from rest_framework.decorators import detail_route
import django_filters
from django.contrib.auth.models import User
from api.models import Sense, Artist, Place, Song, Domain, SemanticClass, Example, Annotation, Dictionary
from api.serializers import SenseSerializer, UserSerializer, ArtistSerializer, PlaceSerializer, SongSerializer, \
    DomainSerializer, SemanticClassSerializer, ExampleSerializer, ExampleHyperlinkedSerializer, AnnotationSerializer, \
    DictionarySerializer
from api.permissions import IsOwnerOrReadOnly
from api.utils import slugify, make_uri


class SenseViewSet(viewsets.ModelViewSet):
    """
    This viewset automatically provides `list`, `create`, `retrieve`,
    `update` and `destroy` actions.

    Additionally we also provide an extra `highlight` action.
    """
    queryset = Sense.objects.all()
    serializer_class = SenseSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,
                          IsOwnerOrReadOnly,)

    @detail_route(renderer_classes=[renderers.TemplateHTMLRenderer])
    def highlight(self, request, *args, **kwargs):
        sense = self.get_object()
        annotations = sense.annotations.all()
        examples = [
            {
                "ex": a.example,
                "song": a.example.from_song.first(),
                "primary_artist": a.example.from_song.first().primary_artist.first(),
                "feat_artist": a.example.from_song.first().feat_artist.first(),
            } for a in annotations]
        data = {
            'sense': sense,
            'examples': examples,
            'domains': sense.domains.all(),
            'semantic_classes': sense.semantic_classes.all(),
            'synonyms': sense.synonyms.all(),
            'antonyms': sense.antonyms.all(),
            'hypernyms': sense.hypernyms.all(),
            'hyponyms': sense.hyponyms.all(),
            'holonyms': sense.holonyms.all(),
            'meronyms': sense.meronyms.all()
        }
        return Response(data, template_name="sense.html")

    def perform_create(self, serializer):
        headword_slug = slugify(serializer.validated_data['headword'])
        serializer.save(owner=self.request.user, headword_slug=headword_slug)


class ArtistFilter(filters.FilterSet):
    name = django_filters.CharFilter(name="name", lookup_expr='contains')

    class Meta:
        model = Artist
        fields = []


class ArtistViewSet(viewsets.ModelViewSet):
    queryset = Artist.objects.all()
    serializer_class = ArtistSerializer
    filter_backends = (filters.DjangoFilterBackend,)
    filter_class = ArtistFilter
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,
                          IsOwnerOrReadOnly,)

    @detail_route(renderer_classes=[renderers.TemplateHTMLRenderer])
    def highlight(self, request, *args, **kwargs):
        artist = self.get_object()
        data = {
            "artist": artist,
            "origin": artist.origin.first(),
            "primary_songs": artist.primary_songs.all(),
            "featured_songs": artist.featured_songs.all(),
        }
        return Response(data, template_name="artist.html")

    def perform_create(self, serializer):
        slug = slugify(serializer.validated_data['name'])
        serializer.save(owner=self.request.user, slug=slug)


class PlaceViewSet(viewsets.ModelViewSet):
    queryset = Place.objects.all()
    serializer_class = PlaceSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,
                          IsOwnerOrReadOnly,)

    @detail_route(renderer_classes=[renderers.TemplateHTMLRenderer])
    def highlight(self, request, *args, **kwargs):
        place = self.get_object()
        annotations = place.annotations.all()
        artists = place.artists.all()
        examples = [
            {
                "ex": a.example,
                "song": a.example.from_song.first(),
                "primary_artist": a.example.from_song.first().primary_artist.first(),
                "feat_artist": a.example.from_song.first().feat_artist.first(),
            } for a in annotations]
        data = {
            'place': place,
            'artists': artists,
            'examples': examples,
        }
        return Response(data, template_name="place.html")

    def perform_create(self, serializer):
        slug = slugify(serializer.validated_data['full_name'])
        serializer.save(owner=self.request.user, slug=slug)


class SongFilter(filters.FilterSet):
    lyrics = django_filters.CharFilter(name="lyrics", lookup_expr='contains')
    primary_artist = django_filters.CharFilter(name="primary_artist__name", lookup_expr='contains', )

    class Meta:
        model = Song
        fields = ['album', 'release_date']


class SongViewSet(viewsets.ModelViewSet):
    queryset = Song.objects.all()
    serializer_class = SongSerializer
    filter_backends = (filters.DjangoFilterBackend,)
    filter_class = SongFilter
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,
                          IsOwnerOrReadOnly,)

    @detail_route(renderer_classes=[renderers.TemplateHTMLRenderer])
    def highlight(self, request, *args, **kwargs):
        song = self.get_object()
        primary_artists = song.primary_artist.all()
        feat_artists = song.feat_artist.all()
        examples = song.examples.all()
        host = request.get_host()
        serializer_data = {
            "text": "",
            "artist": [make_uri(host, 'artists', artist.id) for artist in primary_artists],
            "feat_artist": [make_uri(host, 'artists', artist.id) for artist in feat_artists],
            "from_song": [make_uri(host, 'songs', song.id)]
        }
        example_serializer = ExampleHyperlinkedSerializer(context={'request': request}, data=serializer_data, partial=True)
        example_serializer.is_valid()
        data = {
            "song": song,
            "primary_artists": primary_artists,
            "feat_artists": feat_artists,
            "examples": examples,
            "example_serializer": example_serializer
        }
        return Response(data, template_name="song.html")

    def perform_create(self, serializer):
        artist_names = [a.name for a in serializer.validated_data['primary_artist']]
        slug_text = " ".join(artist_names) + " " + serializer.validated_data['title']
        slug = slugify(slug_text)
        serializer.save(owner=self.request.user, slug=slug)


class DictionaryViewSet(viewsets.ModelViewSet):
    queryset = Dictionary.objects.all()
    serializer_class = DictionarySerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,
                          IsOwnerOrReadOnly,)

    @detail_route(renderer_classes=[renderers.TemplateHTMLRenderer])
    def highlight(self, request, *args, **kwargs):
        dictionary = self.get_object()
        data = {
            "dictionary": dictionary,
            "senses": dictionary.senses.all()
        }
        return Response(data, template_name="dictionary.html")

    def perform_create(self, serializer):
        slug = slugify(serializer.validated_data['name'])
        serializer.save(owner=self.request.user, slug=slug)


class DomainViewSet(viewsets.ModelViewSet):
    queryset = Domain.objects.all()
    serializer_class = DomainSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,
                          IsOwnerOrReadOnly,)

    @detail_route(renderer_classes=[renderers.TemplateHTMLRenderer])
    def highlight(self, request, *args, **kwargs):
        domain = self.get_object()
        data = {
            "domain": domain,
            "senses": domain.senses.all()
        }
        return Response(data, template_name="domain.html")

    def perform_create(self, serializer):
        slug = slugify(serializer.validated_data['name'])
        serializer.save(owner=self.request.user, slug=slug)


class SemanticClassViewSet(viewsets.ModelViewSet):
    queryset = SemanticClass.objects.all()
    serializer_class = SemanticClassSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,
                          IsOwnerOrReadOnly,)

    @detail_route(renderer_classes=[renderers.TemplateHTMLRenderer])
    def highlight(self, request, *args, **kwargs):
        semantic_class = self.get_object()
        data = {
            "semantic_class": semantic_class,
            "senses": semantic_class.senses.all()
        }
        return Response(data, template_name="semantic_class.html")

    def perform_create(self, serializer):
        slug = slugify(serializer.validated_data['name'])
        serializer.save(owner=self.request.user, slug=slug)


class ExampleViewSet(viewsets.ModelViewSet):
    queryset = Example.objects.all()
    serializer_class = ExampleHyperlinkedSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,
                          IsOwnerOrReadOnly,)

    @detail_route(renderer_classes=[renderers.TemplateHTMLRenderer])
    def highlight(self, request, *args, **kwargs):
        example = self.get_object()
        song = example.from_song.first()
        annotations = example.annotations.all()
        host = request.get_host()
        serializer_data = {
            "text": "",
            "start_position": "0",
            "end_position": len(example.text),
            "example": make_uri(host, 'examples', example.id)
        }
        annotation_serializer = AnnotationSerializer(context={'request': request}, data=serializer_data, partial=True)
        annotation_serializer.is_valid()
        data = {
            'example': example,
            'primary_artists': example.artist.all(),
            'feat_artists': example.feat_artist.all(),
            'song': song,
            'annotations': annotations,
            'annotation_serializer': annotation_serializer
        }
        return Response(data, template_name="example.html")

    def perform_create(self, serializer):
        slug = slugify(serializer.validated_data['text'])
        serializer.save(owner=self.request.user, slug=slug)


class AnnotationViewSet(viewsets.ModelViewSet):
    queryset = Annotation.objects.all()
    serializer_class = AnnotationSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,
                          IsOwnerOrReadOnly,)

    @detail_route(renderer_classes=[renderers.StaticHTMLRenderer])
    def highlight(self, request, *args, **kwargs):
        annotation = self.get_object()
        return Response(annotation.text)

    def perform_create(self, serializer):
        slug = slugify(serializer.validated_data['text'])
        serializer.save(owner=self.request.user, slug=slug)


# User views
class UserViewSet(viewsets.ReadOnlyModelViewSet):
    """
    This viewset automatically provides `list` and `detail` actions.
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer