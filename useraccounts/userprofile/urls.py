#userprofile urls.py
from django.urls import path
from django.contrib.auth import views as auth_views
from django.urls import reverse_lazy
from django.views.generic import TemplateView
from .models import User
from . import views
from . import forms

# applicaton name
app_name = 'userprofile'

 # patterns
urlpatterns = [
    # login pattern
    path('login/',views.SingIn.as_view(),name='login'),
    # logout pattern
    path('logout/',auth_views.LogoutView.as_view(),name='logout'),
    # change password pattern
    path('profile/change-password/<int:pk>/', auth_views.PasswordChangeView.
        as_view(template_name='userprofile/PasswordChange.html',
                success_url=reverse_lazy('userprofile:PasswordChangeDone'),
                form_class = forms.FormChangePassword),
                name='PasswordChange'),
    # pattern to inform the password successfully changed
    path('password-changed/',TemplateView.as_view(
                template_name='userprofile/PasswordChangeDone.html'),
                name='PasswordChangeDone'),
    # input email for password rest pattern
    path('reset-password/', auth_views.PasswordResetView.
        as_view(template_name='userprofile/PasswordResetEmail.html',
                success_url=reverse_lazy('userprofile:PasswordEmailSent'),
                form_class = forms.FormRestPassword),
                name='PasswordReset'),
    # pattern to inform that rest password email sent
    path('reset-email-sent/', auth_views.PasswordResetDoneView.
        as_view(template_name='userprofile/PasswordEmailSent.html'),
                name='PasswordEmailSent'),
    # rest password pattern
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.
        as_view(template_name='userprofile/PasswordReset.html',
                success_url=reverse_lazy('index')),
        name='PasswordResetConfirm'),
    # singup pattern
    path('registration/',views.SignUp.as_view(),name='registration'),
    # User Profile details pattern
    path('UserProfile/<int:pk>/',views.ViewProfile.as_view(),name='UserProfileDetails'),
    # Update user proile details pattern
    path('EditUserProfile/<int:pk>/',views.UpdateProfile.as_view(),name='UserProfileEdit'),
    # User account activation pattern
    path('activate/<uidb64>/<token>/',views.ActivateUserAccount,
        name='ActivateUserAccount'),
    # pattern to inform that user account successfully activated
    path('activation-done/',views.TemplateView.
        as_view(template_name='userprofile/ActivationDone.html'),
        name='activation_done'),
    # pattern to inform that email verification email sent
    path('verification-email-sent/',views.TemplateView.
        as_view(template_name='userprofile/VerificationEmailSent.html'),
        name='VerificationEmailSent'),
    # User email verification pattern
    path('verify/<uidb64>/<token>/',views.EmailVerification,
        name='EmailVerification'),
    # send verification email pattern
    path('send-verification-email/<int:pk>/',views.SendVerificationEmail,
        name='SendVerificationEmail'),
    # pattern to inform that user account activation email sent
    path('activation-email-sent/',views.TemplateView.
        as_view(template_name='userprofile/ActivationEmailSent.html'),
        name='ActivationEmailSent'),
    # pattern to inform that user email successfully verified
    path('verification-done/',views.TemplateView.
        as_view(template_name='userprofile/VerificationEmailDone.html'),
        name='VerificationEmailDone'),
]
