#userprofile forms.py
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import ( UserCreationForm,
                                        UserChangeForm,
                                        PasswordChangeForm,
                                        PasswordResetForm,
                                        SetPasswordForm,
                                        )
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from django.urls import reverse
from django import forms
from . import models

class UserSignUp(UserCreationForm):
    '''
    Sign-Up form for new users
    '''
    error_messages = {
        'password_mismatch':"The two password fields didn't match.",
        'email_mismatch': "The two email fields didn't match.",
        }
    email1 = forms.EmailField(
        label="Email",
        widget=forms.EmailInput,
        help_text="Enter your email address.",
    )
    email2 = forms.EmailField(
        label="Confirm Email",
        widget=forms.EmailInput,
        help_text="Enter the same email as before, for verification.",
    )

    class Meta:
        fields = ('first_name', 'last_name', 'email1', 'email2',
                    'username', 'password1', 'password2')
        model = models.User

    def clean_email2(self):
        email1 = self.cleaned_data.get("email1")
        email2 = self.cleaned_data.get("email2")
        if email1 and email2 and email1 != email2:
            raise forms.ValidationError(
                self.error_messages['email_mismatch'],
                code='email_mismatch',
            )
        return email2

    def _post_clean(self):
        super()._post_clean()

        email = self.cleaned_data.get('email2')

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        user.email = self.cleaned_data["email1"]
        if commit:
            user.save()
        return user

class UserProfileForm(UserChangeForm):
    '''
    Profile form to update existing user information
    '''
    error_messages = {
        'email_mismatch': "The two email fields didn't match.",
        }
    email1 = forms.EmailField(
        label="Email",
        widget=forms.EmailInput,
        help_text="Enter your email address.",
    )
    email2 = forms.EmailField(
        label="Confirm Email",
        widget=forms.EmailInput,
        help_text="Enter the same email as before, for verification.",
    )
    password = ReadOnlyPasswordHashField(label="Password")

    class Meta:
        fields = ('first_name','last_name','email1','email2')
        model = models.User

    user = get_user_model()

    def clean_email2(self):
        email1 = self.cleaned_data.get("email1")
        email2 = self.cleaned_data.get("email2")
        if email1 and email2 and email1 != email2:
            raise forms.ValidationError(
                self.error_messages['email_mismatch'],
                code='email_mismatch',
            )
        return email2

    def _post_clean(self):
        super()._post_clean()

        email = self.cleaned_data.get('email2')

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data["email1"]
        if commit:
            user.save()
        return user

    def __init__(self, *args, **kwargs):
        self.user = models.User.objects.get(username=kwargs['instance'])
        super(UserProfileForm, self).__init__(*args, **kwargs)
        print(dir(self.fields['email1']))
        self.fields['email1'].initial = self.user.email
        self.fields['email2'].initial = self.user.email
        if self.user.is_email_verified:
            self.fields['email1'].help_text=('Your email is verified')
        else:
            self.fields['email1'].help_text=(
                                "ATTENTION YOUR EMAIL IS NOT Verified.")
        self.fields['password'].help_text=(
                    "Raw passwords are not stored, so there is no way to see "
                    "this user's password, but you can change the password "
                    "using <a href=\"{}\">this form</a>."
                    .format(reverse(
                        'userprofile:PasswordChange',
                        kwargs={'pk':self.user.pk})))

class FormChangePassword(PasswordChangeForm):
    def __init__(self, *args, **kwargs):
        super(FormChangePassword, self).__init__(*args, **kwargs)
        self.fields['old_password'].label = ('Current Password')

class FormRestPassword(PasswordResetForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['email'].label = ('Enter your email:')
        self.fields['email'].help_text = ('Enter your valid email assigned in your profile.')
