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
        Ensure we can get a single proposition object.
        """
        response = self.client.get('/propositions/1/')
        self.assertEqual(response.data, {'id': 1, 'owner': 'testApiUser', 'title': 'Cats bark', 'truthvalue': False, 'url': 'http://testserver/propositions/1/', 'answers': []})
        
    def test_add_proposition(self):
        """
        Test that we can add a proposition
        """
        response = self.client.post('/propositions/', {'title': 'Moon is square'}, format='json')
        assert response.data['title'] == 'Moon is square'
        assert response.data['truthvalue'] == True
        # Assert 201 Created as status
        assert response.status_code == 201
        self.assertEqual(Proposition.objects.count(), 2)
    
    def test_add_answer(self):
        """
        Tests that we can add an answer
        """
        response = self.client.post('/answers/', {'answer': False, 'proposition': 'http://testserver/propositions/1/'}, format='json')
        # Assert 201 Created as status
        assert response.status_code == 201
        self.assertEqual(Answer.objects.count(), 1)
    
    def test_add_proposition_unauthenticated(self):
        """
        Try to add a Proposition as an unauthenticated user.
        We expect unauthenticated users not to be able to add Propositions.
        """
        self.client.force_authenticate(user=None, token=None)
        response = self.client.post('/propositions/', {'title': 'Unauthenticated users can add Propositions'}, format='json')
        # Assert 403 Permission Denied as status
        assert response.status_code == 403
        # Assert only the initial Proposition exists
        self.assertEqual(Proposition.objects.count(), 1)
    
    def test_add_user_unauthenticated(self):
        """
        Test that an unauthenticated user can add new Users.
        """
        self.client.force_authenticate(user=None, token=None)
        response = self.client.post('/users/', {'username': 'Tahvo', 'password': 'test'}, format='json')
        assert response.data['username'] == 'Tahvo'
        # User password absolutely shouldn't be sent back.
        self.assertFalse('password' in response.data)
        # Assert 201 Created as status
        assert response.status_code == 201
        # We should now have the initial User plus this one
        self.assertEqual(User.objects.count(), 2)
        
    def test_add_user_authenticated(self):
        """
        Test that an authenticated user can add new Users.
        """
        self.client.force_authenticate(user=self.user)
        response = self.client.post('/users/', {'username': 'Kaaleppi', 'password': 'test'}, format='json')
        assert response.data['username'] == 'Kaaleppi'
        # User password absolutely shouldn't be sent back.
        self.assertFalse('password' in response.data)
        # Assert 201 Created as status
        assert response.status_code == 201
        # We should now have the initial User plus this one
        self.assertEqual(User.objects.count(), 2)
    
    def test_everyone_can_access_schema(self):
        """
        Test that the schema is publicly available.
        """
        self.client.force_authenticate(user=None, token=None)
        response = self.client.get('/schema/')
        assert response.status_code == 200
        
    def test_everyone_can_access_docs(self):
        """
        Test that the documentation is publicly available.
        """
        self.client.force_authenticate(user=None, token=None)
        response = self.client.get('/docs/')
        assert response.status_code == 200
    
    def test_everyone_can_access_api_root(self):
        """
        Test that accessing API root will return a list of endpoints.
        """
        self.client.force_authenticate(user=None, token=None)
        response = self.client.get('/')
        assert 'propositions' in response.data