from django.conf.urls import url, include
from rest_framework.routers import DefaultRouter
from api import views


# Create a router and register our viewsets with it.
router = DefaultRouter()
router.register(r'annotations', views.AnnotationViewSet)
router.register(r'artists', views.ArtistViewSet)
router.register(r'domains', views.DomainViewSet)
router.register(r'examples', views.ExampleViewSet)
router.register(r'places', views.PlaceViewSet)
router.register(r'semantic-classes', views.SemanticClassViewSet)
router.register(r'senses', views.SenseViewSet)
router.register(r'songs', views.SongViewSet)
router.register(r'users', views.UserViewSet)


urlpatterns = [

    url(r'^', include(router.urls)),
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework'))

]
