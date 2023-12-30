
from . import views
from django.urls import  path
 
app_name = 'shop' 

urlpatterns = [
    path('products/',views.ProductsShow.as_view(),name='products'),
    path('singleproduct/<int:id>/',views.SingleProduct.as_view(),name='singleproduct')


]
