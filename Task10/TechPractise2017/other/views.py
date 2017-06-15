from django.http import JsonResponse, HttpResponse, HttpResponseRedirect
from django.template import loader
from products.forms import *
from .models import *
from django.shortcuts import render
from .forms import CheckoutContactForm
from django.contrib.auth.models import User
from django.contrib.auth import login, authenticate, logout

def basket_adding(request):
    return_dict = dict()
    session_key = request.session.session_key
    print (request.POST)
    data = request.POST
    product_id = data.get("product_id")
    nmb = data.get("nmb")
    is_delete = data.get("is_delete")

    if is_delete == 'true':
        ProductInBasket.objects.filter(id=product_id).update(is_active=False)
    else:
        new_product, created = ProductInBasket.objects.get_or_create(session_key=session_key, product_id=product_id,
                                                                     is_active=True, defaults={"nmb": nmb})
        if not created:
            print ("not created")
            new_product.nmb += int(nmb)
            new_product.save(force_update=True)

    #common code for 2 cases
    products_in_basket = ProductInBasket.objects.filter(session_key=session_key, is_active=True, order__isnull=True)
    products_total_nmb = products_in_basket.count()
    return_dict["products_total_nmb"] = products_total_nmb

    return_dict["product"] = list()
    for item in  products_in_basket:
        product_dict = dict()
        product_dict["id"] = item.id
        product_dict["name"] = item.product.name
        product_dict["price_per_item"] = item.price_per_item
        product_dict["nmb"] = item.nmb
        return_dict["product"].append(product_dict)

    return JsonResponse(return_dict)
def checkout(request):
    session_key = request.session.session_key
    products_in_basket = ProductInBasket.objects.filter(session_key=session_key, is_active=True, order__isnull=True)
    print (products_in_basket)
    for item in products_in_basket:
        print(item.order)


    form = CheckoutContactForm(request.POST or None)
    if request.POST:
        print(request.POST)
        if form.is_valid():
            print("yes")
            data = request.POST
            name = data.get("name", "3423453")
            phone = data["phone"]
            user, created = User.objects.get_or_create(username=phone, defaults={"first_name": name})

            order = Order.objects.create(user=user, customer_name=name, customer_phone=phone, status_id=1)

            for name, value in data.items():
                if name.startswith("product_in_basket_"):
                    product_in_basket_id = name.split("product_in_basket_")[1]
                    product_in_basket = ProductInBasket.objects.get(id=product_in_basket_id)
                    print(type(value))

                    product_in_basket.nmb = value
                    product_in_basket.order = order
                    product_in_basket.save(force_update=True)

                    ProductInOrder.objects.create(product=product_in_basket.product, nmb = product_in_basket.nmb,
                                                  price_per_item=product_in_basket.price_per_item,
                                                  total_price = product_in_basket.total_price,
                                                  order=order)

            return HttpResponseRedirect(request.META['HTTP_REFERER'])
        else:
            print("no")
    return render(request, 'orders/checkout.html', locals())

def registration(request):
    template = loader.get_template('auth/registration.html')
    session_key = request.session.session_key
    form = CheckoutContactForm(request.POST or None)
    if request.POST:
        print(request.POST)
        if request.POST["password1"]==request.POST["password2"] :
            print("yes")
            data = request.POST
            name = data.get("username", "3423453")
            email = data.get("email")
            password = data.get("password1")
            phone = data["phone"]
            username = request.POST['username']
            password = request.POST['password1']
            us = authenticate(username=email,password=password)
            if us is not None:
                return render(request, 'auth/regestration_falled.html', locals())
            else:
                finish =loader.get_template( 'auth/registration_sucsec.html')
                us = User(username=email, email=email, last_name=phone, first_name=username)
                us.set_password(password)
                us.save()
                request.session['nick']=us.username
                login(request, us)
                checkContext = us.username
                context = {'nick': checkContext, 'form': form}
                return HttpResponse(finish.render(context, request))
        else:
            print("no")
    total_signs = 0
    allProducts = Product.objects.filter(is_active=True )
    for product in allProducts :
        total_signs += product.countVoice
    if request.user.is_anonymous :
        context = {'nick':None,'form':form, 'total_petitions': Product.objects.count(),
                   'total_signs': total_signs}
    else:
        current_user=request.user
        context = {'nick': current_user.first_name,'form':form,'total_petitions': Product.objects.count(),'total_signs': total_signs}
    return HttpResponse(template.render(context, request))

def registration_sucsec(request):
    session_key = request.session.session_key
    return render(request, 'auth/registration_sucsec.html', locals())


def registration_falled(request):
    session_key = request.session.session_key
    return render(request, 'auth/registration_falled.html', locals())


def new_petition(request):
    session_key = request.session.session_key
    form = ProductForm(request.POST or None)
    template = loader.get_template('auth/new_petition.html')
    category = ProductCategory.objects.filter(is_active=True)
    if request.POST:
        name = request.POST["name"]
        category1 = ProductCategory.objects.get(id=request.POST["category"])
        description=request.POST["description"]
        Product.objects.create(name=name,category=category1,description=description,user=request.user)
    total_signs = 0
    finish = loader.get_template('auth/petition_success.html')
    allProducts = Product.objects.filter(is_active=True )
    for product in allProducts :
        total_signs += product.countVoice
    if request.user.is_anonymous :
        context = {'nick':None, 'total_petitions': Product.objects.count(),
                   'total_signs': total_signs,'form':form}
    else:
        current_user=request.user
        context = {'nick': current_user.first_name,'form': form, 'category': category, 'finish': finish, 'total_petitions': Product.objects.count(),'total_signs': total_signs }
    return HttpResponse(template.render(context, request))
def loginUser(request):
    session_key = request.session.session_key
    form = CheckoutContactForm(request.POST or None)
    template = loader.get_template('auth/login.html')
    if request.POST:
         username = request.POST["username"]
         password =request.POST["password1"]
         us = authenticate(username=username, password=password)
         if us is not None:
            login(request,us)
    total_signs = 0
    allProducts = Product.objects.filter(is_active=True )
    for product in allProducts :
        total_signs += product.countVoice
    if request.user.is_anonymous :
        context = {'nick':None, 'total_petitions': Product.objects.count(),
                 'total_signs': total_signs,'form':form}
    else:
         current_user=request.user
         context = {'nick': current_user.first_name,'form':form, 'total_petitions': Product.objects.count(),'total_signs': total_signs}
    return HttpResponse(template.render(context, request))

def logoutUser(request):
    session_key = request.session.session_key
    template = loader.get_template('logout.html')
    logout(request)
    total_signs = 0
    allProducts= Product.objects.all()
    for product in allProducts :
        total_signs += product.countVoice
    if request.user.is_anonymous :
        context = {'nick':None, 'total_petitions': Product.objects.count(),
                   'total_signs': total_signs}
    else:
        current_user=request.user
        context = {'nick': current_user.first_name, 'total_petitions': Product.objects.count(),'total_signs': total_signs}
    return HttpResponse(template.render(context, request))

def petition_sucsec(request):
    session_key = request.session.session_key
    template = loader.get_template('auth/petition_success.html')
    total_signs = 0
    allProducts= Product.objects.all()
    for product in allProducts :
        total_signs += product.countVoice
    if request.user.is_anonymous :
        context = {'nick':None, 'total_petitions': Product.objects.count(),
                   'total_signs': total_signs}
    else:
        current_user=request.user
        context = {'nick': current_user.first_name, 'total_petitions': Product.objects.count(),'total_signs': total_signs}
    return HttpResponse(template.render(context, request))