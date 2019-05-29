"""useraccounts URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.views.generic.base import TemplateView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('users/',include('userprofile.urls')),
    path('',TemplateView.as_view(template_name='index.html'),name='index'),
]

# error handlers
handler404 = TemplateView.as_view(template_name='error_pages/404.html')
handler400 = TemplateView.as_view(template_name='error_pages/400.html')
handler500 = TemplateView.as_view(template_name='error_pages/500.html')
handler403 = TemplateView.as_view(template_name='error_pages/403.html')
