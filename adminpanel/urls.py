
from . import views
from django.urls import  path
from django.views.decorators.cache import never_cache
app_name = 'adminpanel'

urlpatterns = [
    path('dashboard/',never_cache(views.DashBoard.as_view()),name='dashboard'),
    path('admin_login/',never_cache(views.AdminLogin.as_view()),name='admin_login'),
    path('userlist/',views.UserList.as_view(),name='userlist'),
    path('productlist/',views.ProductList.as_view(),name='productlist'),
    path('productadd/',views.ProductAdd.as_view(),name='productadd'),
    path('editproduct/<int:id>/',views.EditProduct.as_view(),name='editproduct'),
    path('coupon/',views.Couponshow.as_view(),name='coupon'),
    path('addcoupon/',views.AddCoupon.as_view(),name='addcoupon'),
    path('deletecoupon/<int:id>/', views.SoftDeleteCoupon.as_view(), name='deletecoupon'),
    path('editcoupn/<int:id>/', views.EditCoupon.as_view(), name='editcoupn'),
    path('add_variant/',views.AddVariant.as_view(),name='add_variant'),
    path('orders/',views.Orders.as_view(),name='orders'),
    path('orderdetails/<int:id>/',views.OrderDetails.as_view(),name='orderdetails'),
    path('refund/<int:id>/',views.Refund.as_view(),name='refund'),
    



]
