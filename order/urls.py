
from . import views
from django.urls import  path

 # Defining the app namespace 
app_name = 'order' 



# URL patterns for the 'order' app
urlpatterns = [
    path('shopcart/',views.ShopyCart.as_view(),name='shopcart'),
    path('addtocart/<int:id>/',views.AddToCart.as_view(),name='addtocart'),
    path('remove_cart/<int:id>/',views.RemoveCart.as_view(),name='remove_cart'),
    path('wishlist/',views.WishListShow .as_view(),name='wishlist'),
    path('addtowishlist/<int:id>/',views.AddToWishList.as_view(),name='addtowishlist'),
    path('checkout/',views.CheckOut.as_view(),name='checkout'),
    path('payment_status/',views.PaymentStatus.as_view(),name='payment_status'),
    path('change_quantity/',views.ChangeQuantity.as_view(),name='change_quantity'),

]
