#userprofile views.py
from django.shortcuts import render, redirect
from django.views.generic import TemplateView, CreateView, UpdateView, RedirectView
from django.urls import reverse_lazy, reverse
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.utils.functional import lazy
from django.http import HttpResponse, HttpResponseRedirect
# imports for user activation
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.views import LogoutView, LoginView
from django.contrib.auth.forms import AuthenticationForm
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
from django import forms as django_forms
from django.contrib import messages
# UserProfile forms and models
from . import forms
from .models import User


# Create your views here.

class SingIn(LoginView):
    '''
    Class view for login
    '''
    # used template
    template_name = 'userprofile/UserLogin.html'

    def post(self, request, *args, **kwargs):
        '''
        Method for posted data
        '''
        # assign variable for form data
        form = self.get_form()
        # Try to get the user details
        try:
            # assign user data to a variable
            user = User.objects.get(
                    username = self.request.POST.get('username'))
            # Check if the user is active
            if not user.is_active:
                # build a content for page details
                content = {'error_message' : 'Inactive',
                            'UnUser': user}
                # send activation email
                SendActivationEmail(self.request,user)
                # display content data
                return render(request, 'userprofile/ActivationError.html',content)
        except:
            # ignore if error occurs
            pass
        # check if form valid
        if form.is_valid():
            # get the valid method
            return self.form_valid(form)
        else:
            # get the invalid method
            return self.form_invalid(form)

class SignUp(CreateView):
    '''
    Class view for registration
    '''
    # Assign signup form
    form_class = forms.UserSignUp
    # used template
    template_name = 'userprofile/UserProfileRegistration.html'

    def form_valid(self, form):
        '''
        Method for valid form
        '''
        # Assign variable for valid form
        user=form.save()
        # save the user data
        user.save()
        # send the activation email
        return SendActivationEmail(self.request,user)


class UpdateProfile(LoginRequiredMixin,UpdateView):
    '''
    Class view to update user details
    '''
    # used template
    template_name = 'userprofile/UserProfileEdit.html'
    # View model
    model = User
    # View form
    form_class = forms.UserProfileForm

    # empty variable for email
    email=str()

    def get_object(self):
        '''
        Method to get the data from the model
        '''
        # Get the current email from user model
        self.email=self.request.user.email
        # return user data
        return self.request.user

    def get_success_url(self):
        '''
        Metho to redirect after a valid form
        '''
        # check if the email is verified
        if self.request.user.is_email_verified==False:
            # send a verification email
            return SendVerificationEmail(self.request,self.request.user)
        else:
            # get the user key
            pk=self.request.user.pk
            # redirect to profile details
            return reverse_lazy('userprofile:profile',kwargs={'pk':pk})

class ViewProfile(LoginRequiredMixin,TemplateView):
    '''
    Class view for profile details
    '''
    # used template
    template_name = 'userprofile/UserProfileDetails.html'

class VerificationEmailSending(LoginRequiredMixin,RedirectView):
    '''
    Class view for sending verification email
    '''
    # used template
    # template_name = 'userprofile/VerificationEmailSending.html'
    def get_redirect_url(self, *args, **kwargs):
        '''
        Method to get the redirect link after sending email
        '''
        # send a verification email
        return SendVerificationEmail(self.request,self.request.user)

def SendActivationEmail(request,user):
    '''
    Function to send activation email
    '''
    # email data
    text_content = 'Account Activation Email'
    subject = 'Email Activation'
    template_name = 'registration/ActivationEmailContent.html'
    from_email = settings.DEFAULT_FROM_EMAIL
    recipients = [user.email]
    # Create token for user activation
    kwargs = {
        'uidb64': urlsafe_base64_encode(force_bytes(user.pk)).decode(),
        'token': default_token_generator.make_token(user)
    }
    # create token link
    activation_url = reverse('userprofile:ActivateUserAccount', kwargs=kwargs)
    # Create full activation link
    activate_url = "{0}://{1}{2}".format(request.scheme, request.get_host(), activation_url)
    # contents for email data
    context = {
        'user': user.first_name,
        'activate_url': activate_url
    }
    # email sending settings
    html_content = render_to_string(template_name, context)
    email = EmailMultiAlternatives(subject, text_content, from_email, recipients)
    email.attach_alternative(html_content, 'text/html')
    email.send()
    print('email sent')
    # return a sent email page after sending
    return redirect('userprofile:ActivationEmailSent')

def ActivateUserAccount(request, uidb64=None, token=None):
    '''
    Function to decode the activation token and activate account
    '''
    # Try to decode the valid token
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    # if token not valid
    except User.DoesNotExist:
        # return an empty user data
        user = None
    # check if user data and token decode available
    if user and default_token_generator.check_token(user, token):
        # verify email
        user.is_email_verified = True
        # activate account
        user.is_active = True
        # save modification to user model
        user.save()
        # login the activated user
        login(request, user)
        # return to activation done page
        return redirect('userprofile:activation_done')
    else:
        # redirect to token expired user data or token not available
        return HttpResponse("Activation link has expired")

def SendVerificationEmail(request,user):
    '''
    Function to send verification email
    '''
    # email data
    text_content = 'Verification Email'
    subject = 'Email Verification'
    template_name = 'registration/VerificationEmailContent.html'
    from_email = settings.DEFAULT_FROM_EMAIL
    recipients = [user.email]
    # Create token for user email verification
    kwargs = {
        'uidb64': urlsafe_base64_encode(force_bytes(user.pk)).decode(),
        'token': default_token_generator.make_token(user)
    }
    # create token link
    verification_url = reverse('userprofile:EmailVerification', kwargs=kwargs)
    # Create full email verification link
    verification_url = "{0}://{1}{2}".format(request.scheme, request.get_host(), verification_url)
    # contents for email data
    context = {
        'user': user.first_name,
        'verification_url': verification_url
    }
    # email sending settings
    html_content = render_to_string(template_name, context)
    email = EmailMultiAlternatives(subject, text_content, from_email, recipients)
    email.attach_alternative(html_content, 'text/html')
    email.send()
    print('email sent')
    # return a sent email page after sending
    return reverse_lazy('userprofile:VerificationEmailSent')

def EmailVerification(request, uidb64=None, token=None):
    '''
    Function to decode the email verification token and verify user email
    '''
    # Try to decode the valid token
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    # if token not valid
    except User.DoesNotExist:
        # return an empty user data
        user = None
    # check if user data and token decode available
    if user and default_token_generator.check_token(user, token):
        # verify email
        user.is_email_verified = True
        # save modification to user model
        user.save()
        # login the user after email verification
        login(request, user)
        # return to email verification done page
        return redirect('userprofile:VerificationEmailDone')
    else:
        # redirect to token expired user data or token not available
        return HttpResponse("Activation link has expired")
