from django.conf.urls import url, include
from django.contrib import admin
from rest_framework import renderers
from rest_framework import routers
from rest_framework import permissions
from rest_framework.schemas import get_schema_view
from rest_framework.routers import DefaultRouter
from rest_framework.urlpatterns import format_suffix_patterns
from rest_framework.response import Response
from rest_framework.reverse import reverse
from factguesser import views
from factguesser.views import PropositionViewSet, UserViewSet, AnswerViewSet, api_root
from rest_framework.documentation import include_docs_urls


router = DefaultRouter()

# Registering Viewsets
router.register(r'propositions', views.PropositionViewSet)
router.register(r'users', views.UserViewSet)
router.register(r'answers', views.AnswerViewSet)

schema_view = get_schema_view(title='Fact listing API', permission_classes=(permissions.AllowAny,))

# The API URLs are determined automatically by the router.
# Additionally, we include the login URLs for the browsable API.
urlpatterns = [
    url(r'^$', api_root),
    url(r'^', include(router.urls)),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^schema/$', schema_view, name='schema'),
    url(r'^docs/', include_docs_urls(title='Fact listing API', public=False, permission_classes=(permissions.AllowAny,))),
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),
]