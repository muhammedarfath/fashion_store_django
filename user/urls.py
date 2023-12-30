
from . import views
from django.contrib import admin
from django.urls import  path
from .handlers import handler404 
from django.views.decorators.cache import never_cache

app_name = 'user'

urlpatterns = [
    path('signup/',views.Signup.as_view(),name='signup'),
    path('login/',never_cache(views.Login.as_view()),name='login'),
    path('logout/', never_cache(views.Logout.as_view()), name='logout'),

]
handler404 = 'user.handlers.handler404'