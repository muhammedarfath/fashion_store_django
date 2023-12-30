
from . import views
from django.urls import  path
 
app_name = 'order' 

urlpatterns = [
    path('shopcart/',views.ShopyCart.as_view(),name='shopcart'),
    path('addtocart/<int:id>/',views.AddToCart.as_view(),name='addtocart'),
    

]
