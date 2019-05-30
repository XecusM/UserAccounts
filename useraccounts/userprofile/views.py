#userprofile views.py
from django.shortcuts import render, redirect
from django.views.generic import TemplateView, CreateView, UpdateView
from django.urls import reverse_lazy, reverse
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.utils.functional import lazy
from django.http import HttpResponse, HttpResponseRedirect
# imports for user activation
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.views import LogoutView
from django.conf import settings
from django.utils.encoding import force_bytes
from django.utils.encoding import force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.core.mail import EmailMultiAlternatives
from django.contrib.auth.tokens import default_token_generator
from django.template.loader import render_to_string
from django.http import HttpResponse, HttpRequest
from django.contrib.sites.shortcuts import get_current_site
from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
# UserProfile forms and models
from . import forms
from .models import User


# Create your views here.

class SignUp(CreateView):
    form_class = forms.UserSignUp
    template_name = 'userprofile/UserProfileRegistration.html'

    def form_valid(self, form):
        user=form.save()
        user.save()
        return SendActivationEmail(self.request,user)


class UpdateProfile(LoginRequiredMixin,UpdateView):
    template_name = 'userprofile/UserProfileEdit.html'
    model = User
    form_class = forms.UserProfileForm

    email=str()

    def get_object(self):
        self.email=self.request.user.email
        return self.request.user

    def get_success_url(self):
        if self.request.user.email != self.email:
            self.request.user.is_email_verified=False
            print('email changed')
            return reverse_lazy('userprofile:VerificationEmailSent')

        elif self.request.user.is_email_verified==False:
            print('email not verfied')
            return reverse_lazy('userprofile:VerificationEmailSent')

        pk=self.request.user.pk
        return reverse_lazy('userprofile:profile',kwargs={'pk':pk})


class ViewProfile(LoginRequiredMixin,TemplateView):
    template_name = 'userprofile/UserProfileDetails.html'

class LogStatus(TemplateView):
    template_name='userprofile/LoginStatus.html'

def SendActivationEmail(request,user):
    text_content = 'Account Activation Email'
    subject = 'Email Activation'
    template_name = 'registration/ActivationEmailContent.html'
    from_email = settings.DEFAULT_FROM_EMAIL
    recipients = [user.email]
    kwargs = {
        'uidb64': urlsafe_base64_encode(force_bytes(user.pk)).decode(),
        'token': default_token_generator.make_token(user)
    }
    activation_url = reverse('userprofile:ActivateUserAccount', kwargs=kwargs)

    activate_url = "{0}://{1}{2}".format(request.scheme, request.get_host(), activation_url)

    context = {
        'user': user.first_name,
        'activate_url': activate_url
    }
    html_content = render_to_string(template_name, context)
    email = EmailMultiAlternatives(subject, text_content, from_email, recipients)
    email.attach_alternative(html_content, 'text/html')
    email.send()
    print('email sent')

    return redirect('userprofile:VerificationEmailSent')

def ActivateUserAccount(request, uidb64=None, token=None):
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except User.DoesNotExist:
        user = None
    if user and default_token_generator.check_token(user, token):
        user.is_email_verified = True
        user.is_active = True
        user.save()
        login(request, user)
        return redirect('userprofile:activation_done')
    else:
        return HttpResponse("Activation link has expired")

def SnedVerificationEmail(request):
    user=request.user
    text_content = 'Verification Email'
    subject = 'Email Verification'
    template_name = 'registration/VerificationEmailContent.html'
    from_email = settings.DEFAULT_FROM_EMAIL
    recipients = [user.email]
    kwargs = {
        'uidb64': urlsafe_base64_encode(force_bytes(user.pk)).decode(),
        'token': default_token_generator.make_token(user)
    }
    verification_url = reverse('userprofile:EmailVerification', kwargs=kwargs)

    verification_url = "{0}://{1}{2}".format(request.scheme, request.get_host(), verification_url)

    context = {
        'user': user.first_name,
        'verification_url': verification_url
    }
    html_content = render_to_string(template_name, context)
    email = EmailMultiAlternatives(subject, text_content, from_email, recipients)
    email.attach_alternative(html_content, 'text/html')
    email.send()
    print('email sent')

    return redirect('userprofile:VerificationEmailSent')

def EmailVerification(request, uidb64=None, token=None):
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except User.DoesNotExist:
        user = None
    if user and default_token_generator.check_token(user, token):
        user.is_email_verified = True
        user.save()
        login(request, user)
        return redirect('userprofile:VerificationEmailDone')
    else:
        return HttpResponse("Activation link has expired")
