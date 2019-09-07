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
        self.email = 'test@email.com'
        self.password = 'Testpass123'

        self.user = get_user_model().objects.create_user(
                                    username=self.username,
                                    first_name=self.first_name,
                                    last_name=self.last_name,
                                    email=self.email,
                                    password=self.password,
                                    is_active=True,
                                    is_email_verified=True
                                    )

        self.index_url = reverse('index')
        self.login_url = reverse('userprofile:login')
        self.registration_url = reverse('userprofile:registration')
        self.profile_details_url = reverse('userprofile:UserProfileDetails',
                                            kwargs={'pk': self.user.pk})
        self.edit_profile_url = reverse('userprofile:UserProfileEdit',
                                            kwargs={'pk': self.user.pk})

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
        self.assertTemplateUsed(response, 'userprofile/UserLogin.html')

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
                                    'email1': 'another@EMAIL.com',
                                    'email2': 'another@EMAIL.com',
                                    'username': 'm.refaat',
                                    'password1': self.password,
                                    'password2': self.password
                                    })

        self.assertRedirects(response,
                            redirect('userprofile:ActivationEmailSent')
                            )

    def test_user_profile_details_get(self):
        '''
        Test get to user profile details page
        '''
        self.client.force_login(self.user)

        response = self.client.get(self.profile_details_url)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response,
                                'userprofile/UserProfileDetails.html')

    def test_user_profile_details_permission(self):
        '''
        Test get to user to another user profile details page
        '''
        user = get_user_model().objects.create_user(
                                    username='m.refaat',
                                    first_name=self.first_name,
                                    last_name=self.last_name,
                                    email='another@email.com',
                                    password=self.password,
                                    is_active=True,
                                    is_email_verified=True
                                    )

        self.client.force_login(user)

        response = self.client.get(self.profile_details_url)

        if response.status_code == 200:
            self.assertEqual(response.status_code, 200)
            self.assertTemplateUsed(response, 'error_pages/403.html')
        else:
            self.assertEqual(response.status_code, 403)

    def test_edit_user_profile_get(self):
        '''
        Test get to edit user profile page
        '''
        self.client.force_login(self.user)

        response = self.client.get(self.edit_profile_url)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response,
                                'userprofile/UserProfileEdit.html')

    def test_edit_user_profile_permission(self):
        '''
        Test get to user to edit another user profile
        '''
        user = get_user_model().objects.create_user(
                                    username='m.refaat',
                                    first_name=self.first_name,
                                    last_name=self.last_name,
                                    email='another@email.com',
                                    password=self.password,
                                    is_active=True,
                                    is_email_verified=True
                                    )

        self.client.force_login(user)

        response = self.client.get(self.edit_profile_url)

        if response.status_code == 200:
            self.assertEqual(response.status_code, 200)
            self.assertTemplateUsed(response, 'error_pages/403.html')
        else:
            self.assertEqual(response.status_code, 403)

    def test_edit_user_profile_post(self):
        '''
        Test pass user registration page
        '''
        self.client.force_login(self.user)

        data = {
            'first_name': 'Osama',
            'last_name': 'Refaat',
            'email1': self.email,
            'email2': self.email,
            'username': self.username,
            'password1': self.password,
            'password2': self.password
        }

        response = self.client.post(self.edit_profile_url, data=data)

        self.assertRedirects(response, self.profile_details_url)

        self.user.refresh_from_db()

        self.assertEquals(self.user.first_name, data['first_name'])
        self.assertEquals(self.user.last_name, data['last_name'])
