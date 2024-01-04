
from . import views
from django.urls import path

 # Defining the app namespace 
app_name = 'home'


# URL patterns for the 'home' app
urlpatterns = [
    path('',views.home,name='home'),
    path('blog/',views.Blog.as_view(),name='blog'),
    path('about_us/',views.AboutUs.as_view(),name='about_us'),
    path('contact/',views.Contact.as_view(),name='contact'),
    path('get_product/',views.Search.as_view(),name='get_product'),


    
]
