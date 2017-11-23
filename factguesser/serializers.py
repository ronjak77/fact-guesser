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
    password = serializers.CharField(write_only=True, style={'input_type': 'password'})

    def create(self, validated_data):
        user = super(UserSerializer, self).create(validated_data)
        user.set_password(validated_data['password'])
        user.save()
        return user

    class Meta:
        model = User
        fields = ('url', 'id', 'username', 'propositions', 'password')
        write_only_fields = ('password',)