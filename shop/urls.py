
from . import views
from django.urls import  path
 
# Defining the app namespace 
app_name = 'shop' 

# URL patterns for the 'shop' app
urlpatterns = [
    path('products/',views.ProductsShow.as_view(),name='products'),
    path('singleproduct/<int:id>/',views.SingleProduct.as_view(),name='singleproduct')
]
