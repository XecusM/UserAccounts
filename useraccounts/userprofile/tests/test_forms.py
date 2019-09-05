#userprofile tests.py
from django.test import TestCase, Client
from django.contrib.auth import get_user_model

from userprofile import forms

class FormsTests(TestCase):
    '''
    Class test for UserAccounts Forms
    '''

    def setUp(self):
        self.client = Client()
        self.username = 'xecus'
        self.first_name = 'Mohamed'
        self.last_name ='Aboel-fotouh'
        self.password = 'Testpassword'
        self.email = 'abo.elfotouh@live.com'

        self.user = get_user_model().objects.create_user(
                                        username=self.username,
                                        first_name=self.first_name,
                                        last_name=self.last_name,
                                        email=self.email,
                                        password=self.password
                                    )

    def test_user_signup_fields(self):
        '''
        Test user SignUp fields
        '''
        expected = ['first_name', 'last_name',
                    'email1', 'email2', 'username',
                    'password1', 'password2']

        actual = list(forms.UserSignUp().fields)

        self.assertSequenceEqual(expected, actual)

    def test_user_signup_form_valid_data(self):
        '''
        test user signup with valid data
        '''
        form = forms.UserSignUp(data={
                                        'first_name': self.first_name,
                                        'last_name': self.last_name,
                                        'email1': 'xecus@OPENMAIL.cc',
                                        'email2': 'xecus@OPENMAIL.cc',
                                        'username': 'm.refaat',
                                        'password1': self.password,
                                        'password2': self.password
                                        })

        self.assertTrue(form.is_valid())

    def test_user_signup_form_invalid_data(self):
        '''
        Test user signup with invalid data
        '''
        form_email = forms.UserSignUp(data={
                                        'first_name': self.first_name,
                                        'last_name': self.last_name,
                                        'email1': 'xecus2@OPENMAIL.cc',
                                        'email2': 'xecus@OPENMAIL.cc',
                                        'username': 'm.refaat',
                                        'password1': self.password,
                                        'password2': self.password
                                        })

        form_first_name = forms.UserSignUp(data={
                                        'first_name': '',
                                        'last_name': self.last_name,
                                        'email1': 'xecus@OPENMAIL.cc',
                                        'email2': 'xecus@OPENMAIL.cc',
                                        'username': 'm.refaat',
                                        'password1': self.password,
                                        'password2': self.password
                                        })

        form_last_name = forms.UserSignUp(data={
                                        'first_name': self.first_name,
                                        'last_name': '',
                                        'email1': 'xecus@OPENMAIL.cc',
                                        'email2': 'xecus@OPENMAIL.cc',
                                        'username': 'm.refaat',
                                        'password1': self.password,
                                        'password2': self.password
                                        })

        form_username = forms.UserSignUp(data={
                                        'first_name': self.first_name,
                                        'last_name': self.last_name,
                                        'email1': 'xecus@OPENMAIL.cc',
                                        'email2': 'xecus@OPENMAIL.cc',
                                        'username': self.username,
                                        'password1': self.password,
                                        'password2': self.password
                                        })

        form_password = forms.UserSignUp(data={
                                        'first_name': self.first_name,
                                        'last_name': self.last_name,
                                        'email1': 'xecus@OPENMAIL.cc',
                                        'email2': 'xecus@OPENMAIL.cc',
                                        'username': 'm.refaat',
                                        'password1': self.password,
                                        'password2': 'anotherpasssword'
                                        })

        self.assertFalse(form_email.is_valid())
        self.assertFalse(form_first_name.is_valid())
        self.assertFalse(form_last_name.is_valid())
        self.assertFalse(form_username.is_valid())
        self.assertFalse(form_password.is_valid())

    def test_user_profile_fields(self):
        '''
        Test user profile fields
        '''
        self.client.force_login(self.user)

        expected = ['first_name', 'last_name',
                    'email1', 'email2', 'password']

        actual = list(forms.UserProfileForm(instance=self.user).fields)

        self.assertSequenceEqual(expected, actual)

    def test_update_user_form_valid_data(self):
        '''
        test update user details with valid data
        '''
        self.client.force_login(self.user)

        form = forms.UserProfileForm(data={
                                        'first_name': self.first_name,
                                        'last_name': self.last_name,
                                        'email1': 'xecus@OPENMAIL.cc',
                                        'email2': 'xecus@OPENMAIL.cc'
                                    }, instance=self.user)

        self.assertTrue(form.is_valid())

    def test_update_user_form_invalid_data(self):
        '''
        Test update user details with invalid data
        '''
        self.client.force_login(self.user)

        form_email = forms.UserProfileForm(data={
                                        'first_name': self.first_name,
                                        'last_name': self.last_name,
                                        'email1': 'xecus2@OPENMAIL.cc',
                                        'email2': 'xecus@OPENMAIL.cc'
                                    }, instance=self.user)

        form_first_name = forms.UserProfileForm(data={
                                        'first_name': '',
                                        'last_name': self.last_name,
                                        'email1': self.email,
                                        'email2': self.email
                                    }, instance=self.user)

        form_last_name = forms.UserProfileForm(data={
                                        'first_name': self.first_name,
                                        'last_name': '',
                                        'email1': self.email,
                                        'email2': self.email
                                    }, instance=self.user)

        self.assertFalse(form_email.is_valid())
        self.assertFalse(form_first_name.is_valid())
        self.assertFalse(form_last_name.is_valid())

    def test_change_password_form_valid_data(self):
        '''
        Test change user password with valid data
        '''
        self.client.force_login(self.user)

        form = forms.FormChangePassword(data={
                                        'old_password': self.password,
                                        'new_password1': 'newtestpassword',
                                        'new_password2': 'newtestpassword',
                                    }, user=self.user)

        self.assertTrue(form.is_valid())

    def test_change_password_form_invalid_data(self):
        '''
        Test change user password with invalid data
        '''
        self.client.force_login(self.user)

        form_old = forms.FormChangePassword(data={
                                    'old_password': 'anotherpasssword',
                                    'new_password1': 'newtestpassword',
                                    'new_password2': 'newtestpassword',
                                }, user=self.user)

        form_new = forms.FormChangePassword(data={
                                    'old_password': self.password,
                                    'new_password1': 'newtestpassword',
                                    'new_password2': 'newtestpass',
                                }, user=self.user)

        self.assertFalse(form_old.is_valid())
        self.assertFalse(form_new.is_valid())

    def test_reset_password_form_valid_data(self):
        '''
        Test reset user password with valid data
        '''

        form = forms.FormRestPassword(data={
                                        'email': self.email
                                        })

        self.assertTrue(form.is_valid())

    def test_reset_password_form_invalid_data(self):
        '''
        Test reset user password with invalid data
        '''
        form = forms.FormRestPassword(data={
                                        'email': 'xecus@openmail'
                                        })

        self.assertFalse(form.is_valid())
