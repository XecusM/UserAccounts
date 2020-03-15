# userprofile test_urls.py
from django.test import TestCase
from django.urls import reverse, resolve

from django.contrib.auth import views as auth_views
from userprofile import views


class UserProfilesUrlsTests(TestCase):
    '''
    Test all urls
    '''

    def test_login_resolved(self):
        '''
        Test login url
        '''
        url = reverse('userprofile:login')
        self.assertEquals(resolve(url).func.view_class, views.SingIn)

    def test_logout_resolved(self):
        '''
        Test logout url
        '''
        url = reverse('userprofile:logout')
        self.assertEquals(resolve(url).func.view_class, auth_views.LogoutView)

    def test_change_password_resolved(self):
        '''
        Test user change password url
        '''
        url = reverse(
                    'userprofile:PasswordChange',
                    kwargs={'pk': 1}
        )
        self.assertEquals(
                        resolve(url).func.view_class,
                        views.PasswordChange
        )

    def test_reset_password_resolved(self):
        '''
        Test user reset password url
        '''
        url = reverse('userprofile:PasswordReset')
        self.assertEquals(resolve(url).func.view_class, views.PasswordReset)

    def test_reset_password_email_sent_resolved(self):
        '''
        Test user reset password email sent url
        '''
        url = reverse('userprofile:PasswordEmailSent')
        self.assertEquals(
                        resolve(url).func.view_class,
                        views.PasswordEmailSent
        )

    def test_reset_password_confirm_resolved(self):
        '''
        Test user reset password comfirm url
        '''
        url = reverse(
                    'userprofile:PasswordResetConfirm',
                    kwargs={'uidb64': 'uidb64', 'token': 'token'}
        )
        self.assertEquals(
                        resolve(url).func.view_class,
                        auth_views.PasswordResetConfirmView
        )

    def test_registration_resolved(self):
        '''
        Test user registration url
        '''
        url = reverse('userprofile:registration')
        self.assertEquals(resolve(url).func.view_class, views.SignUp)

    def test_view_user_profile_resolved(self):
        '''
        Test view user profile url
        '''
        url = reverse(
                    'userprofile:UserProfileDetails',
                    kwargs={'pk': 1}
        )
        self.assertEquals(
                        resolve(url).func.view_class,
                        views.ViewProfile
        )

    def test_edit_user_profile_resolved(self):
        '''
        Test edit user profile url
        '''
        url = reverse(
                    'userprofile:UserProfileEdit',
                    kwargs={'pk': 1}
        )
        self.assertEquals(
                        resolve(url).func.view_class,
                        views.UpdateProfile
        )

    def test_activate_user_resolved(self):
        '''
        Test activate user  url
        '''
        url = reverse(
                    'userprofile:ActivateUserAccount',
                    kwargs={'uidb64': 'uidb64', 'token': 'token'}
        )
        self.assertEquals(
                        resolve(url).func,
                        views.ActivateUserAccount
        )

    def test_verify_user_email_resolved(self):
        '''
        Test verify user email url
        '''
        url = reverse(
                    'userprofile:EmailVerification',
                    kwargs={'uidb64': 'uidb64', 'token': 'token'}
        )
        self.assertEquals(
                        resolve(url).func,
                        views.EmailVerification
        )

    def test_send_verification_email_resolved(self):
        '''
        Test send verification email url
        '''
        url = reverse(
                    'userprofile:SendVerificationEmail',
                    kwargs={'pk': 1}
        )
        self.assertEquals(
                        resolve(url).func.view_class,
                        views.VerificationEmailSending
        )
