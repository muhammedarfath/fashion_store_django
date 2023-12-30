from django.http import HttpResponse
from django.shortcuts import redirect, render ,get_object_or_404
from django.views import View
from shop.models import Product
from order.models import Cart, ShopCart
from django.contrib import messages
from django.core.exceptions import ObjectDoesNotExist

# Create your views here.
def _cart_id(request):
    cart = request.session.session_key
    if not cart:
        cart = request.session.create()
    return cart

class ShopyCart(View):
    def get(self,request):
        current_user = request.user
        try:
            if current_user.is_authenticated:
                cart_item = ShopCart.objects.filter(user=current_user)
            else:
                cart = Cart.objects.get(cart_id=_cart_id(request))    
                cart_item = ShopCart.objects.filter(cart_item=cart)
        except ObjectDoesNotExist:
            pass
        
        context = {
            'cart_item':cart_item
        }
        return render(request,'cart.html',context)

  
  
  
class AddToCart(View):  
    def get(self,request,id):
        return render(request,'cart.html')
        
    def post(self,request,id):
        current_user = request.user
        if request.method == 'POST':
            product = Product.objects.get(id=id)
            if current_user.is_authenticated:
                cart_item = ShopCart.objects.filter(user=current_user,product=product)
                if cart_item:
                    cart_item.quantity += 1
                    cart_item.save()
                    return redirect('/order/shopcart/')  
                else:
                    new_item=ShopCart()  
                    new_item.user=current_user
                    new_item.product=product
                    new_item.quantity=1
                    new_item.save()
                    return redirect('/order/shopcart/')
            else:
                try:
                    cart =  Cart.objects.get(cart_id =_cart_id(request))    
                except Cart.DoesNotExist:
                    cart = Cart.objects.create(cart_id =_cart_id(request))   
                    
                cart.save()     
                cart_item = ShopCart.objects.filter(cart_item=cart,product=product)
                if cart_item:
                    cart_item.quantity += 1
                    cart_item.save()
                    return redirect('/order/shopcart/')  
                else:
                    new_item=ShopCart()  
                    new_item.cart_item=cart
                    new_item.product=product
                    new_item.quantity=1
                    new_item.save()
                    return redirect('/order/shopcart/') 
                  
                
                
        else:
            return self.get(request,id)    
            


            
            
            
                
       
    