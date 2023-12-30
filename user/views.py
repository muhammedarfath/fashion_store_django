import random
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.views import View
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.http import Http404
from order.models import Cart, ShopCart
from order.views import _cart_id
from .forms import SignupForm
from django.views.decorators.cache import never_cache
from django.utils.decorators import method_decorator


# User signup area
class Signup(View):
    def get(self, request):
        return render(request, "signup.html")
        
    def post(self, request):
        if request.method == 'POST':
            form = SignupForm(request.POST)
            if form.is_valid():
                form.save()
                messages.success(request, 'Your account has been created!')
                return redirect('/')
            else:
                messages.warning(request, form.errors)
                return redirect('/user/signup/')


# User login area and checking cart item
@method_decorator(never_cache, name='dispatch')       
class Login(View):
    def get(self, request):
        return render(request, 'index.html')

    def post(self, request):
        if request.method == 'POST':
            name = request.POST.get('name')
            password = request.POST.get('password')
            
            if name.strip() == '' or password.strip() == '':
                messages.warning(request, 'Please fill in all required fields.')
                return redirect('/')
            
            user = authenticate(request, username=name, password=password)
            
            if user is not None:
                try:
                    cart = Cart.objects.get(cart_id=_cart_id(request))
                    is_cart_item_exists = ShopCart.objects.filter(cart_item=cart).exists()
                    if is_cart_item_exists:
                        cart_item = ShopCart.objects.filter(cart_item=cart)
                        products = []
                        exist_products = []
                        for pro in cart_item:
                            product = pro.product
                            products.append(product)
                            
                        cart_item = ShopCart.objects.filter(user=user)
                        for pro in cart_item:
                            product = pro.product
                            exist_products.append(product)
                            
                        for rs in products:
                            if rs in exist_products:
                                cart_item = ShopCart.objects.get(user=user)
                                cart_item.quantity += 1
                                cart_item.cart_item = cart
                                cart_item.save()
                            else:
                                cart_item = ShopCart.objects.filter(cart_item=cart)
                                for item in cart_item:
                                    item.user = user
                                    item.save()        
                                     
                except:
                    pass        
                login(request, user)
                messages.success(request, 'Login successful')
                return redirect('/')
            else:
                messages.error(request, 'Invalid login credentials')
                return redirect('/')

        raise Http404("Page not found") 



# User logout and using never cache 
@method_decorator(never_cache, name='dispatch')          
class Logout(View):
    def get(self, request):
        logout(request)
        return redirect('/')
