from django.contrib.auth.models import User, Group
from rest_framework import serializers
from factguesser.models import Proposition, Answer

class AnswerSerializer(serializers.HyperlinkedModelSerializer):
    """
    Defines a serializer for the Answer model
    """
    owner = serializers.ReadOnlyField(source='owner.username')
    propositiontext = serializers.ReadOnlyField(source='proposition.title')

    class Meta:
        model = Answer
        fields = ('url', 'id', 'answer', 'owner', 'proposition', 'propositiontext', 'created',)
        read_only_fields = ('created', 'propositiontext')

class PropositionSerializer(serializers.HyperlinkedModelSerializer):
    """
    Defines a serializer for the Proposition model
    """
    owner = serializers.ReadOnlyField(source='owner.username')
    # Each Proposition may have related Answers
    answers = serializers.StringRelatedField(many=True, read_only=True)

    class Meta:
        model = Proposition
        fields = ('url', 'id', 'owner', 'title', 'truthvalue', 'answers')
        depth = 2

class UserSerializer(serializers.HyperlinkedModelSerializer):
    """
    Defines a serializer for the User model
    """
    propositions = serializers.HyperlinkedRelatedField(many=True, view_name='proposition-detail', read_only=True)
    # Password input type for Browsable API. User shouldn't be able to retrieve the password, so write_only.
    password = serializers.CharField(write_only=True, style={'input_type': 'password'})
    
    # When user is created, the password is set with set_password
    def create(self, validated_data):
        user = super(UserSerializer, self).create(validated_data)
        user.set_password(validated_data['password'])
        user.save()
        return user

    class Meta:
        model = User
        fields = ('url', 'id', 'username', 'propositions', 'password')
        write_only_fields = ('password',)