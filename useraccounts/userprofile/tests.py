#userprofile tests.py
from django.test import TestCase, SimpleTestCase
from django.urls import reverse, resolve
from .models import User
from .forms import UserSignUp, UserProfileForm
from . import views
# Create your tests here.

class TestModels(TestCase):
    '''
    Class for testing User model
    '''

    def test_create_superuser(self):
        '''
        This test method to test new superuser creation
        '''
        # Create New SuperUser
        self.SuperUser1 = User.objects.create_superuser(
            username = 'xecus',
            first_name = 'Mohamed',
            last_name = 'Aboel-fotouh',
            email = 'abo.elfotouh@live.com',
            password = 'testpassword12345'
        )
        # Test New SuperUser default values
        self.assertTrue(self.SuperUser1.is_superuser)
        self.assertTrue(self.SuperUser1.is_active)
        self.assertTrue(self.SuperUser1.is_email_verified)
        self.assertTrue(self.SuperUser1.is_staff)

    def test_create_user(self):
        '''
        This test method to test new user creation
        '''
        # Create New User
        self.User1 = User.objects.create_user(
            username = 'xecusm',
            first_name = 'Mohamed',
            last_name = 'Aboel-fotouh',
            email = 'xecus@aol.com',
            password = 'testpassword12345'
        )
        # Test New User default values
        self.assertFalse(self.User1.is_superuser)
        self.assertFalse(self.User1.is_active)
        self.assertFalse(self.User1.is_email_verified)
        self.assertFalse(self.User1.is_staff)

class TestForms(TestCase):
    '''
    Class test for UserAccounts Forms
    '''
    def test_UserSignUp_fields(self):
        form = UserSignUp()
        expected = ['first_name', 'last_name',
                    'email1', 'email2', 'username',
                    'password1', 'password2']
        actual = list(form.fields)
        self.assertSequenceEqual(expected, actual)
