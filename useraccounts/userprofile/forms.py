#userprofile forms.py
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import ( UserCreationForm,
                                        UserChangeForm,
                                        PasswordChangeForm,
                                        PasswordResetForm,
                                        SetPasswordForm,
                                        )
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from . import models

class UserSignUp(UserCreationForm):
    '''
    Sign-Up form for new users
    '''
    class Meta:
        fields = ('first_name','last_name','email','username','password1','password2')
        model = models.User

class UserProfileForm(UserChangeForm):
    '''
    Profile form to update existing user information
    '''
    password = ReadOnlyPasswordHashField(label= ("Password"),
        help_text= ("Raw passwords are not stored, so there is no way to see "
                    "this user's password, but you can change the password "
                    "using the following link"))

    class Meta:
        fields = ('first_name','last_name','email')
        model = models.User

    user = get_user_model()

    def __init__(self, *args, **kwargs):
        self.user = models.User.objects.get(username=kwargs['instance'])
        super(UserProfileForm, self).__init__(*args, **kwargs)
        print(kwargs)
        if self.user.is_email_verified:
            self.fields['email'].help_text=('Your email is verified')
        else:
            self.fields['email'].help_text=("ATTENTION YOUR EMAIL IS NOT Verified.")

class FormChangePassword(PasswordChangeForm):
    def __init__(self, *args, **kwargs):
        super(FormChangePassword, self).__init__(*args, **kwargs)
        self.fields['old_password'].label = ('Current Password')

class FormRestPassword(PasswordResetForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['email'].label = ('Enter your email:')
        self.fields['email'].help_text = ('Enter your valid email assigned in your profile.')
