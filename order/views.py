from django.http import HttpResponse
from django.shortcuts import redirect, render ,get_object_or_404
from django.views import View
from shop.models import Product
from order.models import ShopCart
from django.contrib import messages
# Create your views here.

class ShopyCart(View):
    def get(self,request):
        cart_item = ShopCart.objects.all()
        context={
            'cart_item':cart_item,
        }
        return render(request,'cart.html',context)

  
class AddToCart(View):
    def _cart_id(request):
        cart = request.session.session_key
        if not cart:
            cart = request.session.create()
        return cart
        
    def get(self,request,id):
        return render(request,'cart.html')
        
    def post(self,request,id):
        if request.method == 'POST':
            product = Product.objects.get(id=id)
            cart_item = ShopCart.objects.filter(user=request.user,product=product)
            if cart_item:
                cart_item.quantity += 1
                cart_item.save()
                return redirect('/order/shopcart/')  
            else:
                new_item=ShopCart()  
                new_item.user=request.user
                new_item.product=product
                new_item.quantity=1
                new_item.save()
                return redirect('/order/shopcart/')    
        else:
            return self.get(request,id)    
            


            
            
            
                
       
    