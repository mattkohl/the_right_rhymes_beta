from django.contrib.auth.models import User
from rest_framework import permissions, renderers, viewsets, filters
from rest_framework.decorators import detail_route, list_route
from rest_framework.response import Response

from api.filters import ArtistFilter, SongFilter, PlaceFilter, SenseFilter, ExampleFilter
from api.models import Sense, Artist, Place, Song, Domain, SemanticClass, Annotation, Dictionary, Example
from api.forms import ArtistForm, PlaceForm
from api.serializers import SenseSerializer, UserSerializer, ArtistSerializer, PlaceSerializer, \
    SongSerializer, DomainSerializer, SemanticClassSerializer, AnnotationSerializer, DictionarySerializer, \
    ExampleSerializer
from api.utils import slugify, extract_rhymes, clean_up_date, build_example_serializer, \
    build_annotation_serializer, build_examples_from_annotations, \
    build_examples_from_queryset, build_songs_from_queryset


class SenseViewSet(viewsets.ModelViewSet):
    """
    This viewset automatically provides `list`, `create`, `retrieve`,
    `update` and `destroy` actions.

    Additionally we also provide an extra `highlight` action.
    """
    queryset = Sense.objects.all()
    serializer_class = SenseSerializer
    filter_backends = (filters.DjangoFilterBackend,)
    filter_class = SenseFilter
    permission_classes = (permissions.IsAuthenticated,)

    @list_route(renderer_classes=[renderers.TemplateHTMLRenderer])
    def search(self, request, *args, **kwargs):
        queryset = self.queryset.order_by('headword')
        q = self.request.query_params.get('q', None)
        if q is not None:
            queryset = queryset.filter(definition__icontains=q)
        data = {
            "label": "Senses",
            "senses": queryset
        }
        return Response(data, template_name="api/_search.html")

    @detail_route(renderer_classes=[renderers.TemplateHTMLRenderer])
    def highlight(self, request, *args, **kwargs):
        sense = self.get_object()
        annotations = sense.annotations.all()
        rhymes = extract_rhymes(annotations)
        examples = build_examples_from_annotations(annotations, request)
        data = {
            'sense': sense,
            'examples': examples,
            'rhymes': rhymes,
            'domains': sense.domains.all(),
            'semantic_classes': sense.semantic_classes.all(),
            'synonyms': sense.synonyms.all(),
            'antonyms': sense.antonyms.all(),
            'hypernyms': sense.hypernyms.all(),
            'hyponyms': sense.hyponyms.all(),
            'holonyms': sense.holonyms.all(),
            'meronyms': sense.meronyms.all()
        }
        return Response(data, template_name="api/sense.html")

    def perform_create(self, serializer):
        headword_slug = slugify(serializer.validated_data['headword'])
        serializer.save(owner=self.request.user, headword_slug=headword_slug)


class ArtistViewSet(viewsets.ModelViewSet):
    queryset = Artist.objects.all()
    serializer_class = ArtistSerializer
    filter_backends = (filters.DjangoFilterBackend,)
    filter_class = ArtistFilter
    permission_classes = (permissions.IsAuthenticated,)

    @list_route(renderer_classes=[renderers.TemplateHTMLRenderer])
    def search(self, request, *args, **kwargs):
        queryset = self.queryset.order_by('name')
        q = self.request.query_params.get('q', None)
        form = ArtistForm()
        if q is not None:
            queryset = queryset.filter(name__icontains=q)
        data = {
            "label": "Artists",
            "artists": queryset,
            "form": form,
            "form_action": "artist-list"
        }
        return Response(data, template_name="api/_search.html")

    @detail_route(renderer_classes=[renderers.TemplateHTMLRenderer])
    def highlight(self, request, *args, **kwargs):
        artist = self.get_object()
        annotations = artist.annotations.all()
        rhymes = extract_rhymes(annotations)
        examples = build_examples_from_annotations(annotations, request)
        data = {
            "artist": artist,
            "also_known_as": artist.also_known_as.all(),
            "members": artist.members.all(),
            "member_of": artist.member_of.all(),
            "annotations": annotations,
            "rhymes": rhymes,
            "examples": examples,
            "origin": artist.origin,
            "primary_songs": build_songs_from_queryset(artist.primary_songs.order_by('release_date'), request, None),
            "featured_songs": build_songs_from_queryset(artist.featured_songs.order_by('release_date'), request, None),
        }
        return Response(data, template_name="api/artist.html")

    def perform_create(self, serializer):
        slug = slugify(serializer.validated_data['name'])
        serializer.save(owner=self.request.user, slug=slug)


class PlaceViewSet(viewsets.ModelViewSet):
    queryset = Place.objects.all()
    serializer_class = PlaceSerializer
    filter_backends = (filters.DjangoFilterBackend,)
    filter_class = PlaceFilter
    permission_classes = (permissions.IsAuthenticated,)

    @list_route(renderer_classes=[renderers.TemplateHTMLRenderer])
    def search(self, request, *args, **kwargs):
        queryset = self.queryset.order_by('name')
        q = self.request.query_params.get('q', None)
        form = PlaceForm()
        if q is not None:
            queryset = queryset.filter(full_name__icontains=q)
        data = {
            "label": "Places",
            "places": queryset,
            "form": form,
            "form_action": "place-list"
        }
        return Response(data, template_name="api/_search.html")

    @detail_route(renderer_classes=[renderers.TemplateHTMLRenderer])
    def highlight(self, request, *args, **kwargs):
        place = self.get_object()
        annotations = place.annotations.all()
        rhymes = extract_rhymes(annotations)
        contains = place.contains.all()
        within = place.within.all()
        artists = place.artists.all()
        examples = build_examples_from_annotations(annotations, request)
        data = {
            'place': place,
            'contains': contains,
            'within': within,
            'artists': artists,
            'rhymes': rhymes,
            'examples': examples,
        }
        return Response(data, template_name="api/place.html")

    def perform_create(self, serializer):
        full_name = serializer.validated_data['full_name']
        name = full_name.split(", ")[0]
        slug = slugify(full_name)
        serializer.save(owner=self.request.user, slug=slug, name=name)


class SongViewSet(viewsets.ModelViewSet):
    queryset = Song.objects.all()
    serializer_class = SongSerializer
    filter_backends = (filters.DjangoFilterBackend,)
    filter_class = SongFilter
    permission_classes = (permissions.IsAuthenticated,)

    @list_route(renderer_classes=[renderers.TemplateHTMLRenderer])
    def search(self, request, *args, **kwargs):
        queryset = self.queryset.order_by('title')
        q = self.request.query_params.get('q', None)
        data = {"label": "Songs"}
        if q is not None:
            titles = queryset.filter(title__icontains=q)
            lyrics = queryset.filter(lyrics__icontains=q).order_by('release_date')
            data['song_titles'] = build_songs_from_queryset(titles, request, "")
            data['song_lyrics'] = build_songs_from_queryset(lyrics, request, q)
        else:
            data['song_titles'] = build_songs_from_queryset(queryset, request, "")

        return Response(data, template_name="api/_search.html")

    @detail_route(renderer_classes=[renderers.TemplateHTMLRenderer])
    def highlight(self, request, *args, **kwargs):
        song = self.get_object()
        primary_artists = song.primary_artists.all()
        featured_artists = song.featured_artists.all()
        examples = song.examples.all()
        example_serializer = build_example_serializer(request, song, "")
        data = {
            "song": song,
            "primary_artists": primary_artists,
            "featured_artists": featured_artists,
            "examples": examples,
            "example_serializer": example_serializer
        }
        return Response(data, template_name="api/song.html")

    def perform_create(self, serializer):
        release_date_string = serializer.validated_data['release_date_string']
        release_date = clean_up_date(release_date_string)
        artist_names = [a.name for a in serializer.validated_data['primary_artists']]
        slug_text = " ".join(artist_names) + " " + serializer.validated_data['title']
        slug = slugify(slug_text)
        serializer.save(owner=self.request.user, slug=slug, release_date=release_date)


class DictionaryViewSet(viewsets.ModelViewSet):
    queryset = Dictionary.objects.all()
    serializer_class = DictionarySerializer
    permission_classes = (permissions.IsAuthenticated,)

    @detail_route(renderer_classes=[renderers.TemplateHTMLRenderer])
    def highlight(self, request, *args, **kwargs):
        dictionary = self.get_object()
        data = {
            "dictionary": dictionary,
            "senses": dictionary.senses.all()
        }
        return Response(data, template_name="api/dictionary.html")

    def perform_create(self, serializer):
        slug = slugify(serializer.validated_data['name'])
        serializer.save(owner=self.request.user, slug=slug)


class DomainViewSet(viewsets.ModelViewSet):
    queryset = Domain.objects.all()
    serializer_class = DomainSerializer
    permission_classes = (permissions.IsAuthenticated,)

    @list_route(renderer_classes=[renderers.TemplateHTMLRenderer])
    def search(self, request, *args, **kwargs):
        queryset = self.queryset.order_by('name')
        q = self.request.query_params.get('q', None)
        if q is not None:
            queryset = queryset.filter(name__icontains=q)
        data = {
            "label": "Domains",
            "domains": queryset
        }
        return Response(data, template_name="api/_search.html")

    @detail_route(renderer_classes=[renderers.TemplateHTMLRenderer])
    def highlight(self, request, *args, **kwargs):
        domain = self.get_object()
        data = {
            "domain": domain,
            "senses": domain.senses.all()
        }
        return Response(data, template_name="api/domain.html")

    def perform_create(self, serializer):
        slug = slugify(serializer.validated_data['name'])
        serializer.save(owner=self.request.user, slug=slug)


class SemanticClassViewSet(viewsets.ModelViewSet):
    queryset = SemanticClass.objects.all()
    serializer_class = SemanticClassSerializer
    permission_classes = (permissions.IsAuthenticated,)

    @list_route(renderer_classes=[renderers.TemplateHTMLRenderer])
    def search(self, request, *args, **kwargs):
        queryset = self.queryset.order_by('name')
        q = self.request.query_params.get('q', None)
        if q is not None:
            queryset = queryset.filter(name__icontains=q)
        data = {
            "label": "Semantic Classes",
            "semantic_classes": queryset
        }
        return Response(data, template_name="api/_search.html")

    @detail_route(renderer_classes=[renderers.TemplateHTMLRenderer])
    def highlight(self, request, *args, **kwargs):
        semantic_class = self.get_object()
        data = {
            "semantic_class": semantic_class,
            "senses": semantic_class.senses.all()
        }
        return Response(data, template_name="api/semantic_class.html")

    def perform_create(self, serializer):
        slug = slugify(serializer.validated_data['name'])
        serializer.save(owner=self.request.user, slug=slug)


class ExampleViewSet(viewsets.ModelViewSet):
    queryset = Example.objects.all()
    serializer_class = ExampleSerializer
    filter_backends = (filters.DjangoFilterBackend,)
    filter_class = ExampleFilter
    permission_classes = (permissions.IsAuthenticated,)

    @list_route(renderer_classes=[renderers.TemplateHTMLRenderer])
    def search(self, request, *args, **kwargs):
        queryset = self.queryset
        q = self.request.query_params.get('q', None)
        if q is not None:
            queryset = queryset.filter(text__icontains=q)
        data = {
            "label": "Examples",
            "examples": build_examples_from_queryset(queryset, request)
        }
        return Response(data, template_name="api/_search.html")

    @detail_route(renderer_classes=[renderers.TemplateHTMLRenderer])
    def highlight(self, request, *args, **kwargs):
        example = self.get_object()
        song = example.from_song
        annotations = example.annotations.all()
        rhymes = extract_rhymes(annotations)
        annotation_serializer = build_annotation_serializer(request, example)
        annotation_serializer.is_valid()
        data = {
            'example': example,
            'primary_artists': example.primary_artists.all(),
            'featured_artists': example.featured_artists.all(),
            'song': song,
            'annotations': annotations,
            'rhymes': rhymes,
            'annotation_serializer': annotation_serializer
        }
        return Response(data, template_name="api/example.html")

    def perform_create(self, serializer):
        text = serializer.validated_data['text']
        song = serializer.validated_data['from_song']
        slug = slugify(text)
        # check = Example.objects.filter(text=text, from_song__in=song)
        # if check is None:
        #     serializer.save(owner=self.request.user, slug=slug)
        # else:
        #     return redirect('/')
        serializer.save(owner=self.request.user, slug=slug)


class AnnotationViewSet(viewsets.ModelViewSet):
    queryset = Annotation.objects.all()
    serializer_class = AnnotationSerializer
    permission_classes = (permissions.IsAuthenticated,)

    @list_route(renderer_classes=[renderers.TemplateHTMLRenderer])
    def search(self, request, *args, **kwargs):
        queryset = self.queryset
        q = self.request.query_params.get('q', None)
        if q is not None:
            queryset = queryset.filter(text__icontains=q)
        data = {
            "label": "Annotations",
            "annotations": queryset
        }
        return Response(data, template_name="api/_search.html")

    @detail_route(renderer_classes=[renderers.TemplateHTMLRenderer])
    def highlight(self, request, *args, **kwargs):
        annotation = self.get_object()
        data = {
            "annotation": annotation
        }
        return Response(data, template_name="api/annotation.html")

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
