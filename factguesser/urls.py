from django.conf.urls import url, include
from factguesser import views
from rest_framework.routers import DefaultRouter
from factguesser.views import PropositionViewSet, PropositionCountView, UserViewSet
from rest_framework import renderers
from rest_framework.urlpatterns import format_suffix_patterns

# Create a router and register our viewsets with it.
router = DefaultRouter()
router.register(r'propositions', views.PropositionViewSet)
router.register(r'users', views.UserViewSet)

# The API URLs are now determined automatically by the router.
# Additionally, we include the login URLs for the browsable API.
urlpatterns = [
    url(r'^', include(router.urls)),
    url(r'^proposition-count', views.PropositionCountView, name='propositioncount'),
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework'))
]