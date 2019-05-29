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
    template_name = 'UserProfile/sign-up.html'

    def form_valid(self, form):
        user=form.save()
        user.save()
        return send_activation_email(self.request,user)


class UpdateProfile(LoginRequiredMixin,UpdateView):
    template_name = 'UserProfile/edit-profile.html'
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
            return reverse_lazy('UserProfile:verification_email_sent')

        elif self.request.user.is_email_verified==False:
            print('email not verfied')
            return reverse_lazy('UserProfile:verification_email_sent')

        username=self.request.user.pk
        return reverse_lazy('UserProfile:profile',kwargs={'username':username})


class ViewProfile(LoginRequiredMixin,TemplateView):
    template_name = 'UserProfile/profile.html'


class LogStatus(TemplateView):
    template_name='UserProfile/log-status.html'

class LogoutMyView(LogoutView):


    def __init_(self):
        try:
            del self.request.session['heurisitc']
            del self.request.session['data_analysis']
        except:
            pass

def user_login(request):
    # messege = {'messege':'','color': 'white'}
    messege = {'messege':'','status':''}
    if request.method == 'POST':
        # First get the username and password supplied
        username = request.POST.get('username')
        password = request.POST.get('password')

        # Django's built-in authentication function:
        user_authentication = authenticate(username=username, password=password)
        # If we have a user
        if User.objects.filter(username=username).exists():
            #Check it the account is active
            user = User.objects.get(username=username)
            if user.is_active:
                # Log the user in.
                try:
                    login(request,user_authentication)
                    request.session['heuristic']={'function':{},'test':{},'settings':{},'results':{}}
                    request.session['data_analysis']={}
                except:
                    # if username and password didn't match
                    messege['status']='reject'
                    return render(request,'UserProfile/log-status.html',messege)
                # Send the user back to some page.
                # In this case their homepage.
                # return HttpResponseRedirect(reverse('index'))
                print(request.scheme+request.get_host())
                return HttpResponseRedirect(request.get_full_path())
            else:
                # If account is not active:
                messege['status']='not active'
                send_activation_email(request,user)
                return render(request,'UserProfile/log-status.html',messege)
        else:
            # if username and password didn't match
            messege['status']='not exist'
            return render(request,'UserProfile/log-status.html',messege)

    else:

        return render(request,'index.html')

def send_activation_email(request,user):
    text_content = 'Account Activation Email'
    subject = 'Email Activation'
    template_name = 'registration/user-activation.html'
    from_email = settings.DEFAULT_FROM_EMAIL
    recipients = [user.email]
    kwargs = {
        'uidb64': urlsafe_base64_encode(force_bytes(user.pk)).decode(),
        'token': default_token_generator.make_token(user)
    }
    activation_url = reverse('UserProfile:activate_user_account', kwargs=kwargs)

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

    return redirect('UserProfile:activation_email_sent')

def activate_user_account(request, uidb64=None, token=None):
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
        return redirect('UserProfile:activation_done')
    else:
        return HttpResponse("Activation link has expired")

def send_verification_email(request):
    user=request.user
    text_content = 'Verification Email'
    subject = 'Email Verification'
    template_name = 'registration/email-verification.html'
    from_email = settings.DEFAULT_FROM_EMAIL
    recipients = [user.email]
    kwargs = {
        'uidb64': urlsafe_base64_encode(force_bytes(user.pk)).decode(),
        'token': default_token_generator.make_token(user)
    }
    verification_url = reverse('UserProfile:email_verification', kwargs=kwargs)

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

    return redirect('UserProfile:activation_email_sent')

def email_verification(request, uidb64=None, token=None):
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except User.DoesNotExist:
        user = None
    if user and default_token_generator.check_token(user, token):
        user.is_email_verified = True
        user.save()
        login(request, user)
        return redirect('UserProfile:verification-done')
    else:
        return HttpResponse("Activation link has expired")