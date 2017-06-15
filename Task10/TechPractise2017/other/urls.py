"""test_project URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.10/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url, include
from django.contrib import admin
from . import views

urlpatterns = [

    url(r'^basket_adding/$', views.basket_adding, name='basket_adding'),
    url(r'^checkout/$', views.checkout, name='checkout'),
    url(r'^registration/$', views.registration, name='registration'),
    url(r'^registration_falled/$', views.registration_falled, name='registration_falled'),
    url(r'^registration_sucsec/$', views.registration_sucsec, name='registration_sucsec'),
    url(r'^new_petition/$', views.new_petition, name='new_petition'),
    url(r'^petition_success/$', views.petition_sucsec, name='petition_sucsec'),
    url(r'^login/$', views.loginUser, name='login'),
    url(r'^logout/$', views.logoutUser, name='logout')

]
