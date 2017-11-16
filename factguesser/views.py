from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render
from factguesser.permissions import IsOwnerOrReadOnly
from django.contrib.auth.models import User, Group
from serializers import UserSerializer

from rest_framework import viewsets
from rest_framework.decorators import api_view, permission_classes
from rest_framework.decorators import detail_route, list_route
from rest_framework.renderers import JSONRenderer
from rest_framework.views import APIView
from rest_framework import permissions
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework import renderers
from rest_framework.response import Response
from rest_framework.reverse import reverse
from factguesser.models import Proposition, Answer
from factguesser.serializers import PropositionSerializer, AnswerSerializer
from django.http import Http404
from rest_framework.routers import DefaultRouter

class AnswerViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows answers to be viewed.
    """
    queryset = Answer.objects.all()
    serializer_class = AnswerSerializer

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
    """
    queryset = Proposition.objects.all()
    serializer_class = PropositionSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,
                          IsOwnerOrReadOnly,)
                          
    def pre_save(self, obj):
        obj.user = self.request.user
                          
    @detail_route(renderer_classes=[renderers.StaticHTMLRenderer])
    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)
