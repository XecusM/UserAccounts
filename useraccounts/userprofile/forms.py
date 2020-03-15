# userprofile forms.py
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import (
                                        UserCreationForm,
                                        UserChangeForm,
                                        PasswordChangeForm,
                                        PasswordResetForm,
                                    )
from django.contrib.auth.models import BaseUserManager
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from django.urls import reverse
from django import forms
from nocaptcha_recaptcha.fields import NoReCaptchaField


class UserSignUp(UserCreationForm):
    '''
    Sign-Up form for new users
    '''
    # error messages for email and password matches
    error_messages = {
                'password_mismatch': "The two password fields didn't match.",
                'email_mismatch': "The two email fields didn't match.",
            }
    # create field for email
    email1 = forms.EmailField(
        label="Email",
        widget=forms.EmailInput,
        help_text="Enter your email address.",
    )
    # create field for confirmed email
    email2 = forms.EmailField(
        label="Confirm Email",
        widget=forms.EmailInput,
        help_text="Enter the same email as before, for verification.",
    )
    # reCaptcha field
    captcha = NoReCaptchaField()

    class Meta:
        '''
        Initial fields and model for the form
        '''
        fields = [
                    'first_name', 'last_name', 'email1', 'email2',
                    'username', 'password1', 'password2', 'captcha'
        ]
        model = get_user_model()

    def clean_email2(self):
        '''
        Method for if email and confirmed email are the same
        This method works when confirmed email cleared
        '''
        # get the email from email field
        email1 = BaseUserManager.normalize_email(
                                            self.cleaned_data.get("email1"))
        # get the email from confirmed email field
        email2 = BaseUserManager.normalize_email(
                                            self.cleaned_data.get("email2"))
        # check if both emails are equal
        if email1 and email2 and email1 != email2:
            # give an error message if emails not matches
            raise forms.ValidationError(
                self.error_messages['email_mismatch'],
                code='email_mismatch')
        # return the confirmed email
        return email2

    def _post_clean(self):
        '''
        Method to get the cleaned data from the form
        '''
        # initiate the method data
        super()._post_clean()
        # clean confirmed email
        BaseUserManager.normalize_email(self.cleaned_data.get('email2'))

    def save(self, commit=True):
        '''
        Method to save new user
        '''
        # get the initial method
        user = super().save(commit=False)
        # set the password on the model field
        user.set_password(self.cleaned_data["password1"])
        # set the email on the model field
        user.email = BaseUserManager.normalize_email(
                                                self.cleaned_data["email1"])
        # save user data
        if commit:
            user.save()
        # return back user data
        return user


class UserProfileForm(UserChangeForm):
    '''
    Profile form to update existing user information
    '''
    # error message for email matches
    error_messages = {
                    'email_mismatch': "The two email fields didn't match.",
    }
    # create field for email
    email1 = forms.EmailField(
        label="Email",
        widget=forms.EmailInput,
        help_text="Enter your email address.",
    )
    # get the email from confirmed email field
    email2 = forms.EmailField(
        label="Confirm Email",
        widget=forms.EmailInput,
        help_text="Enter the same email as before, for verification.",
    )
    # hid password field
    password = ReadOnlyPasswordHashField(label="Password")

    class Meta:
        '''
        Initial fields and model for the form
        '''
        fields = ['first_name', 'last_name', 'email1', 'email2']
        model = get_user_model()

    # get current user data
    user = get_user_model()

    def clean_email2(self):
        '''
        Method for if email and confirmed email are the same
        This method works when confirmed email cleared
        '''
        # get the email from email field
        email1 = BaseUserManager.normalize_email(
                                            self.cleaned_data.get("email1"))
        # get the email from confirmed email field
        email2 = BaseUserManager.normalize_email(
                                            self.cleaned_data.get("email2"))
        # check if both emails are equal
        if email1 and email2 and email1 != email2:
            # give an error message if emails not matches
            raise forms.ValidationError(
                self.error_messages['email_mismatch'],
                code='email_mismatch')
        # return the confirmed email
        return email2

    def _post_clean(self):
        '''
        Method to get the cleaned data from the form
        '''
        # initiate the method data
        super()._post_clean()
        # clean confirmed email
        BaseUserManager.normalize_email(self.cleaned_data.get('email2'))

    def save(self, commit=True):
        '''
        Method tosave the edited user data
        '''
        # get the initial method
        user = super().save(commit=False)
        # set the email on the model field
        user.email = BaseUserManager.normalize_email(
                                                self.cleaned_data["email1"])
        # save edited user data
        if commit:
            user.save()
        return user

    def __init__(self, *args, **kwargs):
        '''
        Method for initial values and functions for the SignUp form class
        '''
        # get user data from User model
        self.user = get_user_model().objects.get(username=kwargs['instance'])
        # get the initial form class values
        super(UserProfileForm, self).__init__(*args, **kwargs)
        # Add the current email as the inital email
        self.fields['email1'].initial = self.user.email
        # Add the current email as the intial confirmed email
        self.fields['email2'].initial = self.user.email
        # Check if the email is veriified or not
        if self.user.is_email_verified:
            # give a notification for email confirmation
            self.fields['email1'].help_text = 'Your email is verified'
        else:
            # Give attention for email not confirmed
            self.fields['email1'].help_text = "ATTENTION YOUR EMAIL IS \
                                                NOT Verified."
        # Add help text in the password field for change
        self.fields['password'].help_text = "Raw passwords are not stored, \
                so there is no way to see this user's password, \
                but you can change the password using \
                <a href=\"{}\">this form</a>.".format(
                                        reverse(
                                                'userprofile:PasswordChange',
                                                kwargs={'pk': self.user.pk}))


class FormChangePassword(PasswordChangeForm):
    '''
    Change current password
    '''
    def __init__(self, *args, **kwargs):
        '''
        Give the inital values for the password form class
        '''
        # get the initial form class values
        super(FormChangePassword, self).__init__(*args, **kwargs)
        # rename the label from old password to Current password
        self.fields['old_password'].label = ('Current Password')


class FormRestPassword(PasswordResetForm):
    '''
    Reset the lost password
    '''
    def __init__(self, *args, **kwargs):
        '''
        Give the inital values for the password form class
        '''
        # get the initial form class values
        super().__init__(*args, **kwargs)
        # Change email label from Email to Enter your email
        self.fields['email'].label = 'Enter your email:'
        # Add a help text for the email field
        self.fields['email'].help_text = 'Enter your valid email \
                                            assigned in your profile.'
