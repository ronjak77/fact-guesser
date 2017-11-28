import json
from django.test import TestCase, Client
from factguesser.models import Proposition, Answer
from factguesser.serializers import PropositionSerializer, AnswerSerializer
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.reverse import reverse
from rest_framework.test import APITestCase, APIClient
from django.contrib.auth.models import User

class ModelTestCase(TestCase):
    # This class defines tests for the models.

    def setUp(self):
        # Define the test client and other test variables.
        self.client = Client()
        self.user = User.objects.create(username="testUser")
        
        # Make some initial propositions
        Proposition.objects.create(title='Cats bark', owner=self.user, truthvalue=False)
        Proposition.objects.create(title='Dogs like bones', owner=self.user)

    def test_model_can_create_a_proposition(self):
        # Test that the proposition model can create a proposition.
        self.proposition_title = "Pigs can fly"
        self.proposition = Proposition(title=self.proposition_title, owner=self.user)
        old_count = Proposition.objects.count()
        self.proposition.save()
        new_count = Proposition.objects.count()
        self.assertNotEqual(old_count, new_count)

    def test_model_can_create_an_answer(self):
        # Test that the answer model can create an answer.
        old_count = Answer.objects.count()
        # Add a related proposition so that there exists a linked proposition
        testProposition = Proposition.objects.create(title='Cats bark', owner=self.user, truthvalue=False)
        # Initialize the answer
        self.answerValue = False
        self.answer = Answer(answer=self.answerValue, proposition=testProposition)
        # Saving the answer should result in answer total increasing
        self.answer.save()
        new_count = Answer.objects.count()
        self.assertNotEqual(old_count, new_count)

class APITestCase(APITestCase):
    # This class defines tests for the API routes.
    
    def setUp(self):
        # Define the test client and other test variables.
        self.client = APIClient()
        self.user = User.objects.create(username="testApiUser")
        self.client.force_authenticate(user=self.user)
        
        # Create initial Proposition object
        Proposition.objects.create(title='Cats bark', owner=self.user, truthvalue=False)
        
    def test_list_propositions(self):
        """
        Ensure we can list proposition objects.
        """
        url = reverse('proposition-list')
        response = self.client.get(url)
        assert response.data['count'] == 1
        assert response.status_code == 200
    
    def test_proposition(self):
        """
        Ensure we can list proposition objects.
        """
        response = self.client.get('/propositions/1/')
        self.assertEqual(response.data, {'id': 1, 'owner': 'testApiUser', 'title': 'Cats bark', 'truthvalue': False, 'url': 'http://testserver/propositions/1/', 'answers': []})
        
    def test_add_proposition(self):
        """
        Add a proposition
        """
        response = self.client.post('/propositions/', {'title': 'Moon is square'}, format='json')
        assert response.data['title'] == 'Moon is square'
        assert response.data['truthvalue'] == True
        self.assertEqual(Proposition.objects.count(), 2)
    
    def test_add_answer(self):
        """
        Add an answer
        """
        response = self.client.post('/answers/', {'answer': False, 'proposition': 'http://testserver/propositions/2/'}, format='json')
        print response.data
        self.assertEqual(Answer.objects.count(), 1)