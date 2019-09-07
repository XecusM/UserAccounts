#userprofile views.py
from django.shortcuts import render, redirect
from django.views.generic import (
                                TemplateView, CreateView,
                                UpdateView, RedirectView,
                                DetailView
                                )
from django.contrib.auth.views import (
                                        PasswordChangeView,
                                        PasswordResetDoneView,
                                        PasswordResetView
                                        )
from django.urls import reverse_lazy, reverse
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.utils.functional import lazy
from django.http import HttpResponse, HttpResponseRedirect
# imports for user activation
from django.contrib.auth import login, logout
from django.contrib.auth.views import LoginView
from django.conf import settings
from django.utils.encoding import force_bytes
from django.utils.encoding import force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.core.mail import EmailMultiAlternatives
from django.contrib.auth.tokens import default_token_generator
from django.template.loader import render_to_string
from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404

# UserProfile forms and models

from . import forms


# Help functions here

def check_previous_view(self, url):
    '''
    Function to check the previous url with the expected ones
    '''
    previous_url = self.request.META.get('HTTP_REFERER')
    expected_url = f'{self.request.scheme}://{self.request.get_host()}{url}'
    return previous_url == expected_url


# Create your views here.

class SingIn(UserPassesTestMixin, LoginView):
    '''
    Class view for login
    '''
    # used template
    template_name = 'userprofile/UserLogin.html'

    def test_func(self):
        '''
        Check if user is authenticated or not
        '''
        return not self.request.user.is_authenticated

    def post(self, request, *args, **kwargs):
        '''
        Method for posted data
        '''
        # assign variable for form data
        form = self.get_form()
        # Try to get the user details
        try:
            # assign user data to a variable
            user = get_user_model().objects.get(
                    username = self.request.POST.get('username'))
            # Check if the user is active
            if not user.is_active:
                # build a content for page details
                content = {'error_message' : 'Inactive',
                            'UnUser': user}
                # send activation email
                SendActivationEmail(self.request,user)
                # display content data
                return render(
                            request,
                            'userprofile/ActivationError.html',
                            content
                            )
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


class SignUp(UserPassesTestMixin, CreateView):
    '''
    Class view for registration
    '''
    # Assign signup form
    form_class = forms.UserSignUp
    # used template
    template_name = 'userprofile/UserProfileRegistration.html'

    def test_func(self):
        '''
        Check if user is authenticated or not
        '''
        return not self.request.user.is_authenticated

    def form_valid(self, form):
        '''
        Method for valid form
        '''
        # Assign variable for valid form
        user = form.save()
        # save the user data
        user.save()
        # send the activation email
        return SendActivationEmail(self.request, user)


class UpdateProfile(UserPassesTestMixin, UpdateView):
    '''
    Class view to update user details
    '''
    # used template
    template_name = 'userprofile/UserProfileEdit.html'
    # View model
    model = get_user_model()
    # View form
    form_class = forms.UserProfileForm

    # empty variable for email
    email = str()

    def test_func(self):
        '''
        Check if the requested user is the same as the user object
        '''
        return self.request.user == get_user_model().objects.get(
                                                        pk=self.kwargs['pk']
                                                        )

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
            # redirect to profile details
            return reverse_lazy(
                                'userprofile:UserProfileDetails',
                                kwargs={'pk':self.request.user.pk}
                                )


class ViewProfile(UserPassesTestMixin, DetailView):
    '''
    Class view for profile details
    '''
    # used template
    template_name = 'userprofile/UserProfileDetails.html'
    # View model
    model = get_user_model()

    def test_func(self):
        '''
        Check if the requested user is the same as the user object
        '''
        return self.request.user == get_user_model().objects.get(
                                                        pk=self.kwargs['pk']
                                                        )


class PasswordChange(UserPassesTestMixin, PasswordChangeView):
    '''
    Class view for user change password
    '''
    # used template
    template_name='userprofile/PasswordChange.html'
    # View model
    model = get_user_model()
    # form class
    form_class = forms.FormChangePassword
    # success redirect url
    success_url = reverse_lazy('userprofile:PasswordChangeDone')

    def test_func(self):
        '''
        Check if the requested user is the same as the user object
        '''
        return self.request.user == get_user_model().objects.get(
                                                        pk=self.kwargs['pk']
                                                        )


class PasswordChangeDone(UserPassesTestMixin, TemplateView):
    '''
    Class view for confirms that password changed successfully
    '''
    # used template
    template_name='userprofile/PasswordChangeDone.html'

    def test_func(self):
        '''
        Check if the previous url page was change password url
        '''
        return check_previous_view(
                            self,
                            reverse(
                                    'userprofile:PasswordChange',
                                    kwargs={'pk': self.request.user.pk}
                                    )
                            )


class PasswordReset(UserPassesTestMixin, PasswordResetView):
    '''
    Class view to request a password reset
    '''
    # used template
    template_name='userprofile/PasswordResetEmail.html'
    # form used
    form_class = forms.FormRestPassword
    # success url
    success_url=reverse_lazy('userprofile:PasswordEmailSent')

    def test_func(self):
        '''
        Check if user is authenticated or not
        '''
        return not self.request.user.is_authenticated


class PasswordEmailSent(UserPassesTestMixin, PasswordResetDoneView):
    '''
    Class view to confirm that password email has been sent
    '''
    # used template
    template_name='userprofile/PasswordEmailSent.html'

    def test_func(self):
        '''
        Check if the previous url page was passwrod reset url
        '''
        return check_previous_view(
                            self,
                            reverse('userprofile:PasswordReset')
                            )


class VerificationEmailSending(UserPassesTestMixin, RedirectView):
    '''
    Class view for sending verification email
    '''

    def test_func(self):
        return self.request.user == get_user_model().objects.get(
                                                        pk=self.kwargs['pk']
                                                        )

    def get_redirect_url(self, *args, **kwargs):
        '''
        Method to get the redirect link after sending email
        '''
        # send a verification email
        return SendVerificationEmail(self.request, self.request.user)


class VerificationEmailSent(LoginRequiredMixin, TemplateView):
    '''
    Class view to confirm that verfication email has been sent
    '''
    # used template
    template_name = 'userprofile/VerificationEmailSent.html'


class VerificationEmailDone(UserPassesTestMixin, TemplateView):
    '''
    Class view to confirm that email verfication email done
    '''
    # used template
    template_name = 'userprofile/VerificationEmailDone.html'

    def test_func(self):
        '''
        Check if user's email is verified or not
        '''
        return self.request.user.is_email_verified


class ActivationEmailSent(UserPassesTestMixin, TemplateView):
    '''
    Class view to confirm that verfication email has been sent
    '''
    # used template
    template_name = 'userprofile/ActivationEmailSent.html'

    def test_func(self):
        '''
        Check if user is authenticated or not
        '''
        return not self.request.user.is_authenticated


class ActivationDone(UserPassesTestMixin, TemplateView):
    '''
    Class view to confirm that user account is activated
    '''
    # used template
    template_name = 'userprofile/ActivationDone.html'

    def test_func(self):
        '''
        Check if user is activated or not
        '''
        return self.request.user.is_active


def SendActivationEmail(request, user):
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
    activate_url = f'{request.scheme}://{request.get_host()}{activation_url}'
    # contents for email data
    context = {
        'user': user.first_name,
        'activate_url': activate_url
    }
    # email sending settings
    html_content = render_to_string(template_name, context)
    email = EmailMultiAlternatives(
                                subject, text_content,
                                from_email, recipients
                                )
    email.attach_alternative(html_content, 'text/html')
    email.send()
    # return a sent email page after sending
    return redirect('userprofile:ActivationEmailSent')


def ActivateUserAccount(request, uidb64=None, token=None):
    '''
    Function to decode the activation token and activate account
    '''
    # Try to decode the valid token
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = get_user_model().objects.get(pk=uid)
    # if token not valid
    except get_user_model().DoesNotExist:
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
        return redirect('userprofile:ActivationDone')
    else:
        # redirect to token expired user data or token not available
        return HttpResponse("Activation link has expired")


def SendVerificationEmail(request, user):
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
    verification_url = f'{request.scheme}://{request.get_host()}{verification_url}'
    # contents for email data
    context = {
        'user': user.first_name,
        'verification_url': verification_url
    }
    # email sending settings
    html_content = render_to_string(template_name, context)
    email = EmailMultiAlternatives(
                                subject, text_content,
                                from_email, recipients
                                )
    email.attach_alternative(html_content, 'text/html')
    email.send()
    # return a sent email page after sending
    return reverse_lazy('userprofile:VerificationEmailSent')


def EmailVerification(request, uidb64=None, token=None):
    '''
    Function to decode the email verification token and verify user email
    '''
    # Try to decode the valid token
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = get_user_model().objects.get(pk=uid)
    # if token not valid
    except get_user_model().DoesNotExist:
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
        return HttpResponse('Activation link has expired')
