from django.conf.urls import url, include
from rest_framework import renderers
from rest_framework.schemas import get_schema_view
from rest_framework.routers import DefaultRouter
from rest_framework.urlpatterns import format_suffix_patterns
from factguesser import views
from factguesser.views import PropositionViewSet, UserViewSet, AnswerViewSet

# Create a router and register our viewsets with it.
router = DefaultRouter()
router.register(r'propositions', views.PropositionViewSet)
router.register(r'users', views.UserViewSet)
router.register(r'answers', views.AnswerViewSet)

schema_view = get_schema_view(title='Fact listing API')

# The API URLs are now determined automatically by the router.
# Additionally, we include the login URLs for the browsable API.
urlpatterns = [
    url(r'^', include(router.urls)),
    url(r'^schema/$', schema_view),
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework'))
]