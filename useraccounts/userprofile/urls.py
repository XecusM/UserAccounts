# userprofile urls.py
from django.urls import path
from django.contrib.auth import views as auth_views
from django.urls import reverse_lazy
from . import views

# applicaton name
app_name = 'userprofile'

# patterns
urlpatterns = [
    # login pattern
    path('login/', views.SingIn.as_view(), name='login'),
    # logout pattern
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    # change password pattern
    path(
        'profile/change-password/<int:pk>/',
        views.PasswordChange.as_view(),
        name='PasswordChange'
    ),
    # pattern to inform the password successfully changed
    path(
        'password-changed/',
        views.PasswordChangeDone.as_view(),
        name='PasswordChangeDone'
    ),
    # input email for password rest pattern
    path(
        'reset-password/',
        views.PasswordReset.as_view(),
        name='PasswordReset'
    ),
    # pattern to inform that rest password email sent
    path(
        'reset-email-sent/',
        views.PasswordEmailSent.as_view(),
        name='PasswordEmailSent'
    ),
    # rest password pattern
    path(
        'reset/<uidb64>/<token>/',
        auth_views.PasswordResetConfirmView.as_view(
                template_name='userprofile/PasswordReset.html',
                success_url=reverse_lazy('index')),
        name='PasswordResetConfirm'
    ),
    # singup pattern
    path(
        'registration/',
        views.SignUp.as_view(),
        name='registration'
    ),
    # User Profile details pattern
    path(
        'UserProfile/<int:pk>/',
        views.ViewProfile.as_view(),
        name='UserProfileDetails'
    ),
    # Update user proile details pattern
    path(
        'EditUserProfile/<int:pk>/',
        views.UpdateProfile.as_view(),
        name='UserProfileEdit'
    ),
    # User account activation pattern
    path(
        'activate/<uidb64>/<token>/',
        views.ActivateUserAccount,
        name='ActivateUserAccount'
    ),
    # pattern to inform that user account successfully activated
    path(
        'activation-done/',
        views.ActivationDone.as_view(),
        name='ActivationDone'
    ),
    # pattern to inform that email verification email sent
    path(
        'verification-email-sent/',
        views.VerificationEmailSent.as_view(),
        name='VerificationEmailSent'
    ),
    # User email verification pattern
    path(
        'verify/<uidb64>/<token>/',
        views.EmailVerification,
        name='EmailVerification'
    ),
    # send verification email pattern
    path(
        'send-verification-email/<int:pk>/',
        views.VerificationEmailSending.as_view(),
        name='SendVerificationEmail'
    ),
    # pattern to inform that user account activation email sent
    path(
        'activation-email-sent/',
        views.ActivationEmailSent.as_view(),
        name='ActivationEmailSent'
    ),
    # pattern to inform that user email successfully verified
    path(
        'verification-done/',
        views.VerificationEmailDone.as_view(),
        name='VerificationEmailDone'
    ),
]
