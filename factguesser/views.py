from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render
from factguesser.permissions import IsOwnerOrReadOnly
from django.contrib.auth.models import User, Group
from serializers import UserSerializer

from rest_framework import viewsets
from rest_framework.decorators import api_view
from rest_framework.decorators import detail_route
from rest_framework.views import APIView
from rest_framework import permissions
from rest_framework import renderers
from rest_framework.response import Response
from rest_framework.reverse import reverse
from factguesser.models import Proposition
from factguesser.serializers import SnippetSerializer
from django.http import Http404
from rest_framework.routers import DefaultRouter


class UserViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = User.objects.all().order_by('-date_joined')
    serializer_class = UserSerializer
    
class PropositionViewSet(viewsets.ModelViewSet):
    """
    This viewset automatically provides `list`, `create`, `retrieve`,
    `update` and `destroy` actions.

    Additionally we also provide an extra `highlight` action.
    """
    queryset = Proposition.objects.all()
    serializer_class = SnippetSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,
                          IsOwnerOrReadOnly,)

    @detail_route(renderer_classes=[renderers.StaticHTMLRenderer])
    def highlight(self, request, *args, **kwargs):
        snippet = self.get_object()
        return Response(snippet.highlighted)

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)
        
@api_view(['GET'])
def api_root(request, format=None):
    return Response({
        'users': reverse('user-list', request=request, format=format),
        'propositions': reverse('proposition-list', request=request, format=format)
    })