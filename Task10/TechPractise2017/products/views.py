from django.http import HttpResponse
from django.shortcuts import render
from django.template import loader

from products.models import *
from products.forms import *


def petition(request, petition_id):
    product = Product.objects.get(id=petition_id)
    form=CommentForm(request.POST or None)
    com=comment.objects.filter(petition=product)
    if request.POST :
        form.petition=product
        form.user=request.user
        comment.objects.create(user=form.user,petition=form.petition,description=request.POST["description"])
    template = loader.get_template('petitions/petition.html')
    total_signs = 0
    allProducts= Product.objects.all()
    for prod in allProducts :
        total_signs += prod.countVoice
    if request.user.is_anonymous :
        context = {'nick':None,'form':form,'product':product, 'total_petitions': Product.objects.count(),
                   'total_signs': total_signs}
    else:
        current_user=request.user
        context = {'nick': current_user.first_name,'form':form,'comment':com, 'total_petitions': Product.objects.count(),'total_signs': total_signs, 'product':product }
    return HttpResponse(template.render(context, request))