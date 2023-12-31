from django.http import HttpResponse
from django.shortcuts import redirect, render ,get_object_or_404
from django.views import View
from shop.models import Product
from order.models import Cart, ShopCart, Wishlist
from django.contrib import messages
from django.core.exceptions import ObjectDoesNotExist

# Create your views here.

# Function to get the cart id from the session
def _cart_id(request):
    cart = request.session.session_key
    if not cart:
        cart = request.session.create()
    return cart


# View for displaying the shopping cart
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
    

  
  
# View for adding a product to the shopping cart  
class AddToCart(View):  
    def post(self,request,id):
        current_user = request.user
        if request.method == 'POST':
            product = Product.objects.get(id=id)
            if current_user.is_authenticated:
                cart_item = ShopCart.objects.filter(user=current_user,product=product)
                wislistitem = Wishlist.objects.filter(user=current_user,product=product)
                if wislistitem:
                    wislistitem.delete()
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
            

class RemoveCart(View):
    def get(self,request,id):
        product = Product.objects.get(id=id)
        if request.user.is_authenticated:
            cart_item = ShopCart.objects.get(user=request.user,product=product)
        else:
            cart = Cart.objects.get(cart_id=_cart_id(request))    
            cart_item = ShopCart.objects.filter(cart_item=cart)  

        cart_item.delete()
        messages.success(request,'item removed form cart')
        return redirect('/order/shopcart/')
            
            
class WishListShow(View):
    def get(self,request):
        try:
            current_user = request.user
            if current_user.is_authenticated:
                wishlistitem = Wishlist.objects.filter(user=current_user)     
            else:
                messages.warning(request,'please login')
                return redirect('/')                      
        except Wishlist.DoesNotExist:
            wishlistitem = None  
        context={
            'wishlistitem':wishlistitem
            }           
        return render(request,'wishlist.html',context)              
                

class AddToWishList(View):
    def get(self,request,id):
        current_user = request.user
        if current_user.is_authenticated:
            product = Product.objects.get(id=id)
            wishlistitem = Wishlist.objects.filter(user=current_user,product=product)
            cart_item = ShopCart.objects.filter(user=current_user, product=product)
            if wishlistitem.exists():
                messages.success(request,'this item is already added')
                return redirect('/order/wishlist/')
            elif cart_item:
                messages.success(request,'this item is already added in the cart')
                return redirect('/order/shopcart/')
            else:
                wishlistitem = Wishlist.objects.create(user=current_user,product=product)
                wishlistitem.save()
                messages.success(request,'item added to wishlist')
                return redirect('/order/wishlist/')
        else:
            messages.warning(request,'please login')
            return redirect('/')    
                
    
class CheckOut(View):
    def get(self,request):
        current_user = request.user
        cart_item = ShopCart.objects.filter(user=current_user)
        if current_user.is_authenticated and cart_item:
            context = {
                'cart_item':cart_item
            }
            return render(request,'checkout.html',context)    
        else:
            messages.error(request,'please check login and shopcart')
            return redirect('/order/shopcart/')
        
    def post(self,request):
        current_user = request.user
        if request.method == "POST":
            name = request.POST['name']
            email = request.POST['email']
            phone =request.POST['phone']
            country = request.POST['country']
            state = request.POST['state']
            city = request.POST['city']
            address = request.POST['address']
            
            
                       