from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.template import loader
from django.contrib.auth.models import User
from django.http import JsonResponse, HttpResponse, HttpResponseRedirect
from .forms import SubscriberForm
from products.models import *


def home(request):
    template = loader.get_template('landing/home.html')
    total_signs = 0
    allProducts = Product.objects.filter(is_active=True)
    for product in allProducts:
        total_signs += product.countVoice
    products = Product.objects.filter(is_active=True)
    if request.user.is_anonymous :
        context = {'nick':None, 'total_petitions': Product.objects.count(),
                   'total_signs': total_signs, 'products': products}
    else:
        current_user=request.user
        context = {'nick': current_user.first_name, 'total_petitions': Product.objects.count(),'total_signs': total_signs, 'products':products }
    return HttpResponse(template.render(context, request))


def count_voices(request, petition_id):
     product= Product.objects.get(id=petition_id)
     user=User.objects.get(id= request.user.id)
     try:
         v = votes.objects.get(petition=product, user=user)
     except votes.DoesNotExist:
        product.countVoice += 1
        v=votes(user=user,petition=product)
        v.save()
        product.save()
     return redirect('/')

def my_petitions(request):
    template = loader.get_template("landing/my_petitions.html")
    total_signs = 0
    allProducts = Product.objects.filter(is_active=True)
    for product in allProducts:
        total_signs += product.countVoice
    products = Product.objects.filter(user=request.user)
    if request.user.is_anonymous:
        context = {'nick': None, 'total_petitions': Product.objects.count(),
                   'total_signs': total_signs, 'products': products}
    else:
        current_user = request.user
        context = {'nick': current_user.first_name, 'total_petitions': Product.objects.count(), 'total_signs': total_signs, 'products': products}
    return HttpResponse(template.render(context, request))

def result_petitions(request):
    template = loader.get_template("landing/res_petitions.html")
    total_signs = 0
    allProducts = Product.objects.all()
    for product in allProducts:
        total_signs += product.countVoice
    products = Product.objects.filter(countVoice__gte=200)
    if request.user.is_anonymous:
        context = {'nick': None, 'total_petitions': Product.objects.count(),
                   'total_signs': total_signs, 'products': products}
    else:
        current_user = request.user
        context = {'nick': current_user.first_name, 'total_petitions': Product.objects.count(), 'total_signs': total_signs, 'products': products}
    return HttpResponse(template.render(context, request))
