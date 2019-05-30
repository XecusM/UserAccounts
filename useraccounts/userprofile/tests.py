#userprofile tests.py
from django.test import TestCase, SimpleTestCase
from .models import User
from .forms import (UserSignUp, UserProfileForm,
                    FormChangePassword, FormRestPassword)

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
        self.assertTrue(True, self.SuperUser1.is_superuser)
        self.assertTrue(True, self.SuperUser1.is_active)
        self.assertTrue(True, self.SuperUser1.is_email_verified)
        self.assertTrue(True, self.SuperUser1.is_staff)

    def test_create_user(self):
        '''
        This test method to test new user creation
        '''
        # Create New User
        self.User1 = User.objects.create_superuser(
            username = 'xecusm',
            first_name = 'Mohamed',
            last_name = 'Aboel-fotouh',
            email = 'xecus@aol.com',
            password = 'testpassword12345'
        )
        # Test New User default values
        self.assertFalse(False, self.User1.is_superuser)
        self.assertFalse(False, self.User1.is_active)
        self.assertFalse(False, self.User1.is_email_verified)
        self.assertFalse(False, self.User1.is_staff)
