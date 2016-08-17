from rest_framework import permissions, renderers, viewsets
from rest_framework.response import Response
from rest_framework.decorators import api_view, detail_route
from rest_framework.reverse import reverse
from django.contrib.auth.models import User
from api.models import Sense, Artist, Place, Song, Domain, SemanticClass, Example, Annotation
from api.serializers import SenseSerializer, UserSerializer, ArtistSerializer, PlaceSerializer, SongSerializer, \
    DomainSerializer, SemanticClassSerializer, ExampleSerializer, AnnotationSerializer
from api.permissions import IsOwnerOrReadOnly


@api_view(['GET'])
def api_root(request, format=None):
    return Response({
        'users': reverse('user-list', request=request, format=format),
        'senses': reverse('sense-list', request=request, format=format)
    })


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

    @detail_route(renderer_classes=[renderers.StaticHTMLRenderer])
    def highlight(self, request, *args, **kwargs):
        sense = self.get_object()
        return Response(sense.definition)

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class ArtistViewSet(viewsets.ModelViewSet):
    queryset = Artist.objects.all()
    serializer_class = ArtistSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,
                          IsOwnerOrReadOnly,)

    @detail_route(renderer_classes=[renderers.StaticHTMLRenderer])
    def highlight(self, request, *args, **kwargs):
        artist = self.get_object()
        return Response(artist.name)

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class PlaceViewSet(viewsets.ModelViewSet):
    queryset = Place.objects.all()
    serializer_class = PlaceSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,
                          IsOwnerOrReadOnly,)

    @detail_route(renderer_classes=[renderers.StaticHTMLRenderer])
    def highlight(self, request, *args, **kwargs):
        place = self.get_object()
        return Response(place.name)

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class SongViewSet(viewsets.ModelViewSet):
    queryset = Song.objects.all()
    serializer_class = SongSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,
                          IsOwnerOrReadOnly,)

    @detail_route(renderer_classes=[renderers.TemplateHTMLRenderer])
    def highlight(self, request, *args, **kwargs):
        song = self.get_object()
        primary_artists = song.primary_artist.all()
        feat_artists = song.feat_artist.all()
        data = {
            "release_date": song.release_date_string,
            "title": song.title,
            "lyrics": song.lyrics,
            "primary_artists": primary_artists,
            "feat_artists": feat_artists
        }
        return Response(data, template_name="song_lyrics.html")

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class DomainViewSet(viewsets.ModelViewSet):
    queryset = Domain.objects.all()
    serializer_class = DomainSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,
                          IsOwnerOrReadOnly,)

    @detail_route(renderer_classes=[renderers.StaticHTMLRenderer])
    def highlight(self, request, *args, **kwargs):
        place = self.get_object()
        return Response(domain.name)

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class SemanticClassViewSet(viewsets.ModelViewSet):
    queryset = SemanticClass.objects.all()
    serializer_class = SemanticClassSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,
                          IsOwnerOrReadOnly,)

    @detail_route(renderer_classes=[renderers.StaticHTMLRenderer])
    def highlight(self, request, *args, **kwargs):
        semantic_class = self.get_object()
        return Response(semantic_class.name)

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class ExampleViewSet(viewsets.ModelViewSet):
    queryset = Example.objects.all()
    serializer_class = ExampleSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,
                          IsOwnerOrReadOnly,)

    @detail_route(renderer_classes=[renderers.StaticHTMLRenderer])
    def highlight(self, request, *args, **kwargs):
        example = self.get_object()
        return Response(example.text)

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


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
        serializer.save(owner=self.request.user)


# User views
class UserViewSet(viewsets.ReadOnlyModelViewSet):
    """
    This viewset automatically provides `list` and `detail` actions.
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer