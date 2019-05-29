#userprofile urls.py
from django.urls import path

# applicaton name
app_name = 'userprofile'

 # patterns
urlpatterns = [
    path('logout/',auth_views.LogoutView.as_view(),name='logout'),
    path('profile/change-password/<username>/', auth_views.PasswordChangeView.
        as_view(template_name='UserProfile/change-password.html',
                success_url=reverse_lazy('UserProfile:password_changed'),
                form_class = forms.FormChangePassword),
                name='change_password'),
    path('password-changed/',TemplateView.
        as_view(template_name='UserProfile/password-changed.html'),
                name='password_changed'),
    path('reset-password/', auth_views.PasswordResetView.
        as_view(template_name='UserProfile/send-reset-email.html',
                success_url=reverse_lazy('UserProfile:reset_email_sent'),
                form_class = forms.FormRestPassword),
                name='reset_password'),
    path('reset-email-sent/', auth_views.PasswordResetDoneView.
        as_view(template_name='UserProfile/reset-email-sent.html'),
                name='reset_email_sent'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.
        as_view(template_name='UserProfile/reset-password.html',
                success_url=reverse_lazy('index')),
        name='password_reset_confirm'),
    path('logstatus/',views.LogStatus.as_view(),name='logstatus'),
    path('sign-up/',views.SignUp.as_view(),name='signup'),
    path('profile/<username>/',views.ViewProfile.as_view(),name='profile'),
    path('edit-profile/<username>/',views.UpdateProfile.as_view(),name='edit_profile'),
    path('activate/<uidb64>/<token>/',views.activate_user_account,
        name='activate_user_account'),
    path('activation-done/',views.TemplateView.
        as_view(template_name='UserProfile/activation-done.html'),
        name='activation_done'),
    path('activation-email-sent/',views.TemplateView.
        as_view(template_name='UserProfile/activation-email-sent.html'),
        name='activation_email_sent'),
    path('verify/<uidb64>/<token>/',views.email_verification,
        name='email_verification'),
    path('send-verification-email/<username>/',views.send_verification_email,name='send_verification_email'),
    path('verification-email-sent/',views.send_verification_email,
        name='verification_email_sent'),
    path('verification-done/',views.TemplateView.
        as_view(template_name='UserProfile/verification-done.html'),
        name='verification-done'),
]
