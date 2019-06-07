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
    path('login/',views.SingIn.as_view(),name='login'),
    path('logout/',auth_views.LogoutView.as_view(),name='logout'),
    path('profile/change-password/<int:pk>/', auth_views.PasswordChangeView.
        as_view(template_name='userprofile/PasswordChange.html',
                success_url=reverse_lazy('userprofile:PasswordChangeDone'),
                form_class = forms.FormChangePassword),
                name='PasswordChange'),
    path('password-changed/',TemplateView.as_view(
                template_name='userprofile/PasswordChangeDone.html'),
                name='PasswordChangeDone'),
    path('reset-password/', auth_views.PasswordResetView.
        as_view(template_name='userprofile/PasswordResetEmail.html',
                success_url=reverse_lazy('userprofile:PasswordEmailSent'),
                form_class = forms.FormRestPassword),
                name='PasswordReset'),
    path('reset-email-sent/', auth_views.PasswordResetDoneView.
        as_view(template_name='userprofile/PasswordEmailSent.html'),
                name='PasswordEmailSent'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.
        as_view(template_name='userprofile/PasswordReset.html',
                success_url=reverse_lazy('index')),
        name='PasswordResetConfirm'),
    path('registration/',views.SignUp.as_view(),name='registration'),
    path('UserProfile/<int:pk>/',views.ViewProfile.as_view(),name='UserProfileDetails'),
    path('EditUserProfile/<int:pk>/',views.UpdateProfile.as_view(),name='UserProfileEdit'),
    path('activate/<uidb64>/<token>/',views.ActivateUserAccount,
        name='ActivateUserAccount'),
    path('activation-done/',views.TemplateView.
        as_view(template_name='userprofile/ActivationDone.html'),
        name='activation_done'),
    path('verification-email-sent/',views.TemplateView.
        as_view(template_name='userprofile/VerificationEmailSent.html'),
        name='VerificationEmailSent'),
    path('verify/<uidb64>/<token>/',views.EmailVerification,
        name='EmailVerification'),
    path('send-verification-email/<int:pk>/',views.SendVerificationEmail,
        name='SendVerificationEmail'),
    path('activation-email-sent/',views.TemplateView.
        as_view(template_name='userprofile/ActivationEmailSent.html'),
        name='ActivationEmailSent'),
    path('verification-done/',views.TemplateView.
        as_view(template_name='userprofile/VerificationEmailDone.html'),
        name='VerificationEmailDone'),
]
