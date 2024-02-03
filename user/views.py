import random
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, render, redirect
from django.views import View
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout,update_session_auth_hash
from django.http import Http404
from user.models import Coupon, UserProfile
from order.models import Cart, Country, Order, OrderProduct, ShopCart, State, Town
from order.views import _cart_id
from .forms import SignupForm
from django.views.decorators.cache import never_cache
from django.utils.decorators import method_decorator
from django.contrib.auth.forms import PasswordChangeForm
from django.core.mail import send_mail
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.contrib.auth.tokens import default_token_generator
from django.utils.encoding import force_bytes, force_str
from django.core.mail import EmailMessage

# User signup area
class Signup(View):
    def get(self, request):
        return render(request, "signup.html")
        
    def post(self, request):
        if request.method == 'POST':
            form = SignupForm(request.POST)
            if form.is_valid():
                form.save()
                otp = str(random.randint(100000, 999999))

                request.session['user']=form.cleaned_data['username']
                request.session['signup_otp'] = otp
    
                print(otp)


                subject = 'OTP Verification Code'
                message = f'Your OTP code for signup is: {otp}'
                from_email = 'coloshope@gmail.com'
                recipient_list = [form.cleaned_data['email']]
                
                

                send_mail(subject, message, from_email, recipient_list)
                
                messages.success(request, 'Your account has been created!Please Enter OTP')
                return render(request,'otp.html',{'user':form.cleaned_data['email']})            
            else:
                messages.warning(request, form.errors)
                return redirect('/user/signup/')
            
# After Signup We Can Enter Otp
class Otp(View):
    def post(self,request):
        if request.method == 'POST':
            otp_entered = (
                request.POST['first'] +
                request.POST['second'] +
                request.POST['third'] +
                request.POST['fourth'] +
                request.POST['fifth'] +
                request.POST['sixth']
            )
            otp_saved = request.session.get('signup_otp')
            if otp_entered == otp_saved:
                username=request.session['user']
                user = User.objects.get(username=username)
                user.is_active = True
                user.save()
                messages.success(request, "Your registration is successful. You can now log in.")           
                return redirect('/')  
            else:
                messages.error(request, 'Invalid OTP. Please try again.')

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
            
            user = authenticate(request, username=name, password=password, is_active=True)
            
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

#User Account Details
class Account(View):
    def get(self,request):
        user = request.user
        coupon = Coupon.objects.filter(active=True) 
        form = PasswordChangeForm(user)
        orderproduct = OrderProduct.objects.filter(user=user)
        user_profile = UserProfile.objects.filter(user=user).first()
        context={
            'user':user,
            'account':user_profile,
            'form':form,
            'orderproduct':orderproduct,
            'coupon':coupon
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
        
#User Can Update the Password    
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


#If the user forgot the password at the time of login
class ForgotPassword(View):
    def get(self,request):
        return render(request,'forgot_password.html')
    def post(self,request):
        if request.method == "POST":
                email = request.POST["email"]
                name = request.POST["name"]

                if User.objects.filter(email=email,username=name).exists():
                    user = User.objects.get(email__exact=email,username=name)
 
                    current_site = get_current_site(request)
                    mail_subject = "Reset Your Password"
                    message = render_to_string(
                        "reset_password_email.html",
                        {
                            "user": user,
                            "domain": current_site.domain,
                            "uid": urlsafe_base64_encode(force_bytes(user.pk)),
                            "token": default_token_generator.make_token(user),
                        },
                    )
                    to_email = email
                    send_mail = EmailMessage(mail_subject, message, to=[to_email])
                    send_mail.send()
                    messages.success(
                        request, "Password reset email has been sent to your email address"
                    )
                    return redirect("/")
                else:
                    messages.error(request, "Account does not exist")
                    return redirect("/user/forgotpassword/")

# Reset Password after apply the forgot password                
class ResetpasswordValidate(View):
    def get(self,request,uidb64, token):
        try:
            uid = urlsafe_base64_decode(uidb64).decode()
            user = User._default_manager.get(pk=uid)
        except (TypeError, ValueError, OverflowError, User.DoesNotExist):
            user = None

        if user is not None and default_token_generator.check_token(user, token):
            request.session["uid"] = uid
            messages.success(request, "please reset your password")
            return render(request,'resetpassword.html')
        else:
            messages.success(request, "this link has been expired!")
            return redirect("/")          
           
# Reset Password after apply the forgot password     
class ResetPassword(View):
    def post(self,request):
        if request.method == "POST":
            password = request.POST["password"]
            confirm_password = request.POST["confirm_password"]
            if password == confirm_password:
                uid = request.session.get("uid")
                if uid is not None:
                    user = User.objects.get(pk=uid)
                    user.set_password(password)
                    user.save() 
                messages.success(request, "Password Reset Successful")
                return redirect("/")
            else:
                messages.error(request, "password do not match")
                return redirect("/user/resetpassword/")
        return render(request, "resetpassword.html")
                
                
class CancelOrder(View):
    template_name = 'myaccount.html'

    def post(self, request, id):
        
        url = request.META.get("HTTP_REFERER")
        if request.method == 'POST':
            reason = request.POST.get('cancel_reason')
            if not reason:
                messages.error(request, "Cancel reason is required.")
                return redirect(url)

            orders = get_object_or_404(Order, id=id)
            orders.user_note = reason
            orders.status = "Canceled"
            orders.save()

            # Pass context to render function
            return render(request, self.template_name, {'orders': orders})

            