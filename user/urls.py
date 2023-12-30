# Importing necessary modules and classes
from . import views
from django.contrib import admin
from django.urls import path
from django.views.decorators.cache import never_cache
from .handlers import handler404

# Defining the app namespace
app_name = 'user'

# URL patterns for the 'user' app
urlpatterns = [
    path('signup/', views.Signup.as_view(), name='signup'),         
    path('login/', never_cache(views.Login.as_view()), name='login'),  
    path('logout/', never_cache(views.Logout.as_view()), name='logout'), 
]

# Custom handler for 404 errors
handler404 = 'user.handlers.handler404'