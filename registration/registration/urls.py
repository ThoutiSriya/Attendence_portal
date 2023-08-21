"""registration URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
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
from app1 import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('Facsign', views.Facsign, name='Facsign'),
    path('Stusign', views.Stusign, name='Stusign'),
    path('Facsave', views.Facsave, name='Facsave'),
    path('Stusave', views.Stusave, name='Stusave'),
    path('login', views.LoginPage, name='login'),
    path('login1', views.LoginPage1, name='login1'),
    path('', views.display, name='home'),
    path('Studash', views.Studash, name='Studash'),
    path('detecting', views.detecting, name='detecting'),
    path('viewing', views.viewing, name='viewing')
]

# path('login', views.LoginfPage, name='login'),
# path('saveform', views.save_form, name='saveform'),
