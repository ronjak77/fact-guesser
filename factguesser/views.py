from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render
from django.contrib.auth.models import User, Group
from django.http import Http404
from serializers import UserSerializer
from rest_framework import viewsets
from rest_framework import permissions
from rest_framework import exceptions
from rest_framework import renderers
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.decorators import detail_route, list_route
from rest_framework.renderers import JSONRenderer
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.response import Response
from rest_framework.reverse import reverse
from rest_framework.routers import DefaultRouter
from factguesser.models import Proposition, Answer
from factguesser.serializers import PropositionSerializer, AnswerSerializer
from factguesser.permissions import IsOwnerOrReadOnly, IsSameUserOrReadOnly, AllowAddAndRead

# Explicitly define the api root view, in order to include the schema in the listing.
@api_view(['GET'])
@permission_classes((permissions.AllowAny, ))
def api_root(request, format=None):
    """
    An API for creating Propositions and Answers related to them.
    """
    return Response({
        'users': reverse('user-list', request=request, format=format),
        'propositions': reverse('proposition-list', request=request, format=format),
        'answers': reverse('answer-list', request=request, format=format),
        'schema': reverse('schema', request=request, format=format)
    })

class AnswerViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows answers to be created and viewed.
    """
    queryset = Answer.objects.all()
    serializer_class = AnswerSerializer
    permission_classes = (AllowAddAndRead, )

class UserViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be created, viewed, updated, edited or deleted.
    """
    queryset = User.objects.all().order_by('-date_joined')
    serializer_class = UserSerializer
    permission_classes = (IsSameUserOrReadOnly,)

class PropositionViewSet(viewsets.ModelViewSet):
    """
     API endpoint that allows Propositions to be created, viewed or edited.
    """
    queryset = Proposition.objects.all()
    serializer_class = PropositionSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,
                          IsOwnerOrReadOnly,)
                          
    # On creation, set current user as owner, for permission management purposes
    @detail_route(renderer_classes=[renderers.StaticHTMLRenderer])
    def perform_create(self, serializer):
        if self.request.user.is_authenticated():
            serializer.save(owner=self.request.user)
        else:
            raise exceptions.PermissionDenied(detail=None, code=None)
