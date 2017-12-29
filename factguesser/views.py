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
    Returns a listing of the available endpoints of this Factguesser API.
    
    'Users', 'propositions' and 'answers' are related to the functionality of the API, and you can access data through them.
    
    'Schema' and 'documentation' are there to provide you more information about the API and make it easier to use it. 
    """
    return Response({
        'users': reverse('user-list', request=request, format=format),
        'propositions': reverse('proposition-list', request=request, format=format),
        'answers': reverse('answer-list', request=request, format=format),
        'schema': reverse('schema', request=request, format=format),
        'documentation': reverse('api-docs:docs-index', request=request, format=format),
    })
    

class AnswerViewSet(viewsets.ModelViewSet):
    """
    retrieve: Return the given answer.
    
    list: Return a list of all the answers.
    
    create: Create a new Answer. This requires the URL of the related Proposition.
    """
    queryset = Answer.objects.all()
    serializer_class = AnswerSerializer
    permission_classes = (AllowAddAndRead, )

class UserViewSet(viewsets.ModelViewSet):
    """
    list: List all users.
    
    create: Create a new User. A new User will not have admin privileges but can add Propositions to the system.
    
    read: Return info of a single User.
    
    update: Update the info of an User. Requires you to be logged in as that user.
    
    partial_update: Update some of the info of an User. Requires you to be logged in as that user.
    
    delete: Delete an user. Requires you to be logged in as that user or to be an Admin user.
    
    """
    queryset = User.objects.all().order_by('-date_joined')
    serializer_class = UserSerializer
    permission_classes = (IsSameUserOrReadOnly,)

class PropositionViewSet(viewsets.ModelViewSet):
    """
    list: Lists all the Propositions.
    
    create: Creates a new Proposition. This requires you to be a logged in User.
    
    read: Shows the details of a single Proposition. 
    
    update: Allows editing of a Proposition. You have to be the Proposition's owner or an Admin to be allowed to update it.
    
    partial_update: Allows editing of a Proposition. You have to be the Proposition's owner or an Admin to be allowed to update it.
    
    delete: Allows the owner of the Proposition or an Admin to delete it.
    
    perform_create: Internal function that couldn't be hidden from the documentation. It cannot be accessed through the API by users.
    
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
