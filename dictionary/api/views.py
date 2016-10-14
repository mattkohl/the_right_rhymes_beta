import uuid
from api.filters import ArtistFilter, SongFilter, PlaceFilter, SenseFilter#, ExampleFilter
from api.models import Sense, Artist, Place, Song, Domain, SemanticClass, Annotation, Dictionary#, Example
from api.permissions import IsOwnerOrReadOnly
from api.serializers import SenseSerializer, UserSerializer, ArtistSerializer, PlaceSerializer, SongSerializer, \
    DomainSerializer, SemanticClassSerializer, AnnotationSerializer, \
    DictionarySerializer#, ExampleHyperlinkedSerializer
from api.utils import slugify, make_uri, extract_rhymes, build_annotation_serializer#, build_example_serializer
from django.contrib.auth.models import User
from django.shortcuts import redirect
from rest_framework import permissions, renderers, viewsets, filters, reverse, status
from rest_framework.decorators import detail_route, list_route
from rest_framework.response import Response


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
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,
                          IsOwnerOrReadOnly,)

    @list_route(renderer_classes=[renderers.TemplateHTMLRenderer])
    def search(self, request, *args, **kwargs):
        queryset = Sense.objects.all().order_by('-created')
        q = self.request.query_params.get('q', None)
        if q is not None:
            queryset = queryset.filter(definition__icontains=q)
        data = {
            "senses": queryset
        }
        return Response(data, template_name="sense_search.html")

    @detail_route(renderer_classes=[renderers.TemplateHTMLRenderer])
    def highlight(self, request, *args, **kwargs):
        sense = self.get_object()
        annotations = sense.annotations.all()
        rhymes = extract_rhymes(annotations)
        examples = [
            {
                "ex": a,
                "song": a.song.first(),
                "primary_artist": a.song.first().primary_artist.first(),
                "feat_artist": a.song.first().feat_artist.all(),
            } for a in annotations]
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
        return Response(data, template_name="sense.html")

    def perform_create(self, serializer):
        headword_slug = slugify(serializer.validated_data['headword'])
        serializer.save(owner=self.request.user, headword_slug=headword_slug)


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
        annotations = artist.annotations.all()
        rhymes = extract_rhymes(annotations)
        data = {
            "artist": artist,
            "also_known_as": artist.also_known_as.all(),
            "members": artist.members.all(),
            "member_of": artist.member_of.all(),
            "annotations": annotations,
            "rhymes": rhymes,
            "origin": artist.origin.first(),
            "primary_songs": [
                {
                    "id": song.id,
                    "title": song.title,
                    "release_date": song.release_date_string,
                    "album": song.album,
                    "feat_artist": song.feat_artist.all(),
                } for song in artist.primary_songs.order_by('release_date')
            ],
            "featured_songs": [
                {
                    "id": song.id,
                    "title": song.title,
                    "release_date": song.release_date_string,
                    "album": song.album,
                    "feat_artist": song.feat_artist.all(),
                } for song in artist.featured_songs.order_by('release_date')
            ],
        }
        return Response(data, template_name="artist.html")

    def perform_create(self, serializer):
        slug = slugify(serializer.validated_data['name'])
        serializer.save(owner=self.request.user, slug=slug)


class PlaceViewSet(viewsets.ModelViewSet):
    queryset = Place.objects.all()
    serializer_class = PlaceSerializer
    filter_backends = (filters.DjangoFilterBackend,)
    filter_class = PlaceFilter
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,
                          IsOwnerOrReadOnly,)

    @detail_route(renderer_classes=[renderers.TemplateHTMLRenderer])
    def highlight(self, request, *args, **kwargs):
        place = self.get_object()
        annotations = place.annotations.all()
        rhymes = extract_rhymes(annotations)
        contains = place.contains.all()
        within = place.within.all()
        artists = place.artists.all()
        examples = [
            {
                "ex": a,
                "song": a.song.first(),
                "primary_artist": a.song.first().primary_artist.first(),
                "feat_artist": a.song.first().feat_artist.first(),
            } for a in annotations]
        data = {
            'place': place,
            'contains': contains,
            'within': within,
            'artists': artists,
            'rhymes': rhymes,
            'examples': examples,
        }
        return Response(data, template_name="place.html")

    def perform_create(self, serializer):
        slug = slugify(serializer.validated_data['full_name'])
        serializer.save(owner=self.request.user, slug=slug)


class SongViewSet(viewsets.ModelViewSet):
    queryset = Song.objects.all()
    serializer_class = SongSerializer
    filter_backends = (filters.DjangoFilterBackend,)
    filter_class = SongFilter
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,
                          IsOwnerOrReadOnly,)

    @list_route(renderer_classes=[renderers.TemplateHTMLRenderer])
    def search(self, request, *args, **kwargs):
        q = self.request.query_params.get('q', None)
        data = dict()
        if q is not None:
            queryset = Song.objects.filter(release_date_verified=True).filter(lyrics__icontains=q).order_by('release_date')
            data['results'] = [
                {
                    "song": song,
                    "primary_artist": song.primary_artist.first(),
                    "feat_artist": song.feat_artist.all(),
                    "annotations": [build_annotation_serializer(request, song, line) for line in song.lyrics.split('\n') if q.lower() in line.lower()]
                } for song in queryset]
        else:
            data["results"] = []
        return Response(data, template_name="song_search.html")

    @detail_route(renderer_classes=[renderers.TemplateHTMLRenderer])
    def highlight(self, request, *args, **kwargs):
        song = self.get_object()
        primary_artists = song.primary_artist.all()
        feat_artists = song.feat_artist.all()
        annotations = song.annotations.all()
        annotation_serializer = build_annotation_serializer(request, song, "")
        data = {
            "song": song,
            "primary_artists": primary_artists,
            "feat_artists": feat_artists,
            "annotations": annotations,
            "annotation_serializer": annotation_serializer
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


# class ExampleViewSet(viewsets.ModelViewSet):
#     queryset = Example.objects.all()
#     serializer_class = ExampleHyperlinkedSerializer
#     filter_backends = (filters.DjangoFilterBackend,)
#     filter_class = ExampleFilter
#     permission_classes = (permissions.IsAuthenticatedOrReadOnly,
#                           IsOwnerOrReadOnly,)
#
#     @detail_route(renderer_classes=[renderers.TemplateHTMLRenderer])
#     def highlight(self, request, *args, **kwargs):
#         example = self.get_object()
#         song = example.from_song.first()
#         annotations = example.annotations.all()
#         rhymes = extract_rhymes(annotations)
#         host = request.get_host()
#         serializer_data = {
#             "text": "",
#             "start_position": "0",
#             "end_position": len(example.text),
#             "example": make_uri(host, 'examples', example.id)
#         }
#         annotation_serializer = AnnotationSerializer(context={'request': request}, data=serializer_data, partial=True)
#         annotation_serializer.is_valid()
#         data = {
#             'example': example,
#             'primary_artists': example.artist.all(),
#             'feat_artists': example.feat_artist.all(),
#             'song': song,
#             'annotations': annotations,
#             'rhymes': rhymes,
#             'annotation_serializer': annotation_serializer
#         }
#         return Response(data, template_name="example.html")
#
#     def perform_create(self, serializer):
#         text = serializer.validated_data['text']
#         song = serializer.validated_data['from_song']
#         slug = slugify(text)
#         check = Example.objects.filter(text=text, from_song__in=song)
#         print(check)
#         if len(check) == 0:
#             serializer.save(owner=self.request.user, slug=slug)
#             data = serializer.data
#             headers = self.get_success_headers(serializer.data)
#             return Response(data, status=status.HTTP_201_CREATED, headers=headers)
#         else:
#             serialized = ExampleHyperlinkedSerializer(check.first(), context={'request': request})
#             return Response(serialized.data, status=status.HTTP_303_SEE_OTHER)


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