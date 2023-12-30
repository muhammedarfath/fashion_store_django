
from . import views
from django.urls import  path

 # Defining the app namespace 
app_name = 'order' 



# URL patterns for the 'order' app
urlpatterns = [
    path('shopcart/',views.ShopyCart.as_view(),name='shopcart'),
    path('addtocart/<int:id>/',views.AddToCart.as_view(),name='addtocart'),
    
]
