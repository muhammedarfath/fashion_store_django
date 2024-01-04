# Importing necessary modules and classes
from . import views
from django.contrib import admin
from django.urls import path
from django.views.decorators.cache import never_cache


# Defining the app namespace
app_name = 'user'

# URL patterns for the 'user' app
urlpatterns = [
    path('signup/', views.Signup.as_view(), name='signup'), 
    path('otp/',views.Otp.as_view(),name='otp'),        
    path('login/', never_cache(views.Login.as_view()), name='login'),  
    path('logout/', never_cache(views.Logout.as_view()), name='logout'), 
    path('account/',views.Account.as_view(),name='account'),
    path('updatepassword/',views.UpdatePassword.as_view(),name='updatepassword'),
    path('forgotpassword/',views.ForgotPassword.as_view(),name='forgotpassword'),
    path("resetpassword_validate/<uidb64>/<token>/",views.ResetpasswordValidate.as_view(),name="resetpassword_validate"),
    path('resetpassword/',views.ResetPassword.as_view(),name='resetpassword'),

]

