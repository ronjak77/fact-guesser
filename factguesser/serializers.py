from django.contrib.auth.models import User, Group
from rest_framework import serializers
from factguesser.models import Proposition

class PropositionSerializer(serializers.HyperlinkedModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.username')
    
    class Meta:
        model = Proposition
        fields = ('url', 'id', 'owner', 'title', 'tosi')

class UserSerializer(serializers.HyperlinkedModelSerializer):
    snippets = serializers.HyperlinkedRelatedField(many=True, view_name='proposition-detail', read_only=True)

    class Meta:
        model = User
        fields = ('url', 'id', 'username', 'snippets')
