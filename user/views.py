import random
from django.http import HttpResponse
from django.shortcuts import render,redirect
from django.views import View
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate,login,logout
from django.http import Http404
from .forms import SignupForm
from django.views.decorators.cache import never_cache
from django.utils.decorators import method_decorator
# Create your views here.
class Signup(View):
    def get(self,request):
        return render(request, "signup.html")
        
    def post(self,request):
        if request.method == 'POST':
            form = SignupForm(request.POST)
            if form.is_valid():
                form.save()
                messages.success(request, 'Your account has been created!')
                return redirect('/')
            else:
                messages.warning(request,form.errors)
                return redirect('/user/signup/')

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
                login(request, user)
                messages.success(request, 'Login successful')
                return redirect('/')
            else:
                messages.error(request, 'Invalid login credentials')
                return redirect('/')

        raise Http404("Page not found") 
 
   
@method_decorator(never_cache, name='dispatch')          
class Logout(View):
    def get(self,request):
        logout(request)
        return redirect('/')
                
            
        
