from django.contrib.auth.models import User, Group
from rest_framework import serializers
from factguesser.models import Proposition, Answer

class AnswerSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Answer
        fields = ('url', 'id', 'answer', 'proposition', 'created')
        read_only_fields = ('created',)

class PropositionSerializer(serializers.HyperlinkedModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.username')
    answers = serializers.StringRelatedField(many=True, read_only=True)
    
    class Meta:
        model = Proposition
        fields = ('url', 'id', 'owner', 'title', 'truthvalue', 'answers')
        depth = 2

class UserSerializer(serializers.HyperlinkedModelSerializer):
    propositions = serializers.HyperlinkedRelatedField(many=True, view_name='proposition-detail', read_only=True)

    class Meta:
        model = User
        fields = ('url', 'id', 'username', 'propositions')