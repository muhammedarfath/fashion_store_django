
from . import views
from django.urls import  path

app_name = 'adminpanel'

urlpatterns = [
    path('',views.DashBoard.as_view(),name='dashboard'),
    path('userlist/',views.UserList.as_view(),name='userlist'),
    path('productlist/',views.ProductList.as_view(),name='productlist'),
    path('productadd/',views.ProductAdd.as_view(),name='productadd'),
    path('add_variant/',views.AddVariant.as_view(),name='add_variant'),

    


]
