import random
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, render, redirect
from django.views import View
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout,update_session_auth_hash
from django.http import Http404
from user.models import UserProfile
from order.models import Cart, Country, OrderProduct, ShopCart, State, Town
from order.views import _cart_id
from .forms import SignupForm
from django.views.decorators.cache import never_cache
from django.utils.decorators import method_decorator
from django.contrib.auth.forms import PasswordChangeForm


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


class Account(View):
    def get(self,request):
        user = request.user
        account = UserProfile.objects.get(user = user)
        form = PasswordChangeForm(request.user)
        orderproduct = OrderProduct.objects.filter(user=user)

        context={
            'user':user,
            'account':account,
            'form':form,
            'orderproduct':orderproduct
        }
        return render(request,'myaccount.html',context)    
    
    def post(self,request):
            if request.method == 'POST':
                name = request.POST['name']
                address = request.POST['address']
                phone = request.POST['phone']
                country = request.POST['country']
                state =request.POST['state']
                city = request.POST['city']
                
                requird_fields = [name,phone,country,state,city,address]
                if not all(requird_fields):
                    messages.error(request,'Please fill in all the required fields.')
                    return redirect('/user/account/')            
                country_instance = Country.objects.get(name=country)
                state_instance = State.objects.get(name=state)
                city_instance = Town.objects.get(name=city)            

                user_form = get_object_or_404(User, username=request.user)
                
                # Check if the new username already exists
                if User.objects.exclude(pk=user_form.pk).filter(username=name).exists():
                    return HttpResponse("Username already exists. Choose a different username.")
                user_form.username = name
                user_form.save()

            profile,create = UserProfile.objects.get_or_create(user=user_form)
            profile.phone = phone
            profile.country = country_instance.name
            profile.city = city_instance.name
            profile.state = state_instance.name
            profile.address = address
            profile.save()
            messages.success(request,'profile updated successfully')
            return redirect("/user/account/")        
        
    
class UpdatePassword(View):
    def post(self,request):
        url = request.META.get("HTTP_REFERER")
        if request.method == "POST":
            form = PasswordChangeForm(request.user, request.POST)
            if form.is_valid():
                user = form.save()
                update_session_auth_hash(request, user) 
                messages.success(request, "Your password was successfully updated!")
                return redirect(url)
            else:
                messages.error(
                    request, "Please correct the error below.<br>" + str(form.errors)
                )
                return redirect(url)
        else:
            form = PasswordChangeForm(request.user)
            return render(request, "myaccount.html", {"form": form})    

        