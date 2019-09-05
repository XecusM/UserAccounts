# userprofile test_views.py
from django.test import TestCase, Client
from django.urls import reverse
from django.shortcuts import render, redirect
from django.contrib.auth import get_user_model

from django.contrib.auth import views as auth_views
from userprofile import views

class UserProfilesViewsTests(TestCase):
    '''
    Test all user views
    '''
    def setUp(self):
        '''
        Test intiation
        '''
        self.client = Client()

        self.username = 'xecus'
        self.first_name = 'Mohamed'
        self.last_name = 'Aboel-fotouh'
        self.email = 'abo.elfotouh@live.com'
        self.password = 'Testpass123'

        self.user = get_user_model().objects.create_user(
                                    username=self.username,
                                    first_name=self.first_name,
                                    last_name=self.last_name,
                                    email=self.email,
                                    password=self.password
                                    )

        self.index_url = reverse('index')
        self.login_url = reverse('userprofile:login')
        self.registration_url = reverse('userprofile:registration')

    def test_index_get(self):
        '''
        Test get index page
        '''
        response = self.client.get(self.index_url)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'index.html')


    def test_login_get(self):
        '''
        Test get to login page
        '''
        response = self.client.get(self.login_url)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'userprofile/login.html')

    def test_login_post(self):
        '''
        Test pass login page
        '''
        response = self.client.post(self.login_url, data={
                                    'username': self.username,
                                    'password': self.password
                                    }, follow=True, secure=True)

        self.assertEqual(response.status_code, 200)

    def test_user_registration_get(self):
        '''
        Test get to user registration page
        '''
        response = self.client.get(self.registration_url)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response,
                                'userprofile/UserProfileRegistration.html')

    def test_user_registration_post(self):
        '''
        Test pass user registration page
        '''
        response = self.client.post(self.registration_url, data={
                                    'first_name': self.first_name,
                                    'last_name': self.last_name,
                                    'email1': 'xecus@OPENEMAIL.com',
                                    'email2': 'xecus@OPENEMAIL.com',
                                    'username': 'm.refaat',
                                    'password1': self.password,
                                    'password2': self.password
                                    })

        self.assertEqual(response.status_code, 302)
