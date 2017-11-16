from django.contrib.auth.models import User, Group
from rest_framework import serializers
from factguesser.models import Proposition, Answer

class AnswerSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Answer
        fields = ('answer', 'proposition', 'created')
        read_only_fields = ('answer', 'created')

class PropositionSerializer(serializers.HyperlinkedModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.username')
    answers = serializers.HyperlinkedRelatedField(many=True, view_name='answer-detail', read_only=True)
    
    class Meta:
        model = Proposition
        fields = ('url', 'id', 'owner', 'title', 'truthvalue', 'answers')
        depth = 2

class UserSerializer(serializers.HyperlinkedModelSerializer):
    snippets = serializers.HyperlinkedRelatedField(many=True, view_name='proposition-detail', read_only=True)
    

    class Meta:
        model = User
        fields = ('url', 'id', 'username', 'snippets')