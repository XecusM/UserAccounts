#userprofile tests.py
from django.test import TestCase
from django.urls import reverse, resolve

from userprofile.models import User

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
        self.SuperUser = User.objects.create_superuser(
            username = 'xecus',
            first_name = 'Mohamed',
            last_name = 'Aboel-fotouh',
            email = 'test@email.com',
            password = 'testpassword12345'
        )
        # Test New SuperUser default values
        self.assertTrue(self.SuperUser.is_superuser)
        self.assertTrue(self.SuperUser.is_active)
        self.assertTrue(self.SuperUser.is_email_verified)
        self.assertTrue(self.SuperUser.is_staff)
        self.assertEqual(
            self.SuperUser.get_full_name(),
            f'{self.SuperUser.first_name} {self.SuperUser.last_name}'
        )

    def test_create_user(self):
        '''
        This test method to test new user creation
        '''
        # Create New User
        self.User = User.objects.create_user(
            username = 'xecusm',
            first_name = 'Mohamed',
            last_name = 'Aboel-fotouh',
            email = 'tesst@email.com',
            password = 'testpassword12345'
        )
        # Test New User default values
        self.assertFalse(self.User.is_superuser)
        self.assertFalse(self.User.is_active)
        self.assertFalse(self.User.is_email_verified)
        self.assertFalse(self.User.is_staff)
        self.assertEqual(
            self.User.get_full_name(),
            f'{self.User.first_name} {self.User.last_name}'
        )
