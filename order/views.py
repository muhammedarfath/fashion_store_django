from django.http import HttpResponse, JsonResponse
from django.shortcuts import redirect, render ,get_object_or_404
from django.views import View
from shop.models import Product, Size
from order.models import Cart, Country, Order, OrderProduct, Payment, ShopCart, State, Town, Wishlist
from django.contrib import messages
from django.core.exceptions import ObjectDoesNotExist
import razorpay
import random
import time
from django.conf import settings

# Create your views here.

# Function to get the cart id from the session
def _cart_id(request):
    cart = request.session.session_key
    if not cart:
        cart = request.session.create()
    return cart


# View for displaying the shopping cart
class ShopyCart(View):
    total = 0
    def get(self,request):
        current_user = request.user
        context = {}
        try:
            if current_user.is_authenticated:
                cart_item = ShopCart.objects.filter(user=current_user)
                
            else:
                cart = Cart.objects.get(cart_id=_cart_id(request))    
                cart_item = ShopCart.objects.filter(cart_item=cart)
            for items in cart_item:
                items.single_price = items.product.sale_price * items.quantity 
                self.total += items.product.sale_price * items.quantity 
                items.save()
            tax = (2 * self.total) / 100
            grand_total = self.total + tax
            
            
            request.session['grand_total'] = float(grand_total)
            
            context = {
                'cart_item':cart_item,
                'grand_total':grand_total
            }                
                
        except ObjectDoesNotExist:
            pass

        return render(request,'cart.html',context)
    

  
  
# View for adding a product to the shopping cart  
class AddToCart(View): 
    def post(self,request,id):
        current_user = request.user
        size_id = request.GET.get('size_id') 
        size_instance = Size.objects.get(id=size_id) 
        if request.method == 'POST':
            product = Product.objects.get(id=id)
            if current_user.is_authenticated:
                cart_item = ShopCart.objects.filter(user=current_user,product=product,size=size_instance).first()
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
                    new_item.size = size_instance
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
                    new_item.size = size_instance
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
        if current_user.is_authenticated:
            cart_item = ShopCart.objects.filter(user=current_user)
            if  cart_item:
                grand_total = request.session.get('grand_total') * 100
                context = {
                    'cart_item':cart_item,
                    'grand_total':grand_total
                }
                return render(request,'checkout.html',context)  
            else:
                messages.error(request,'please check shopcart')
                return redirect('/order/shopcart/')                  
        else:
            messages.error(request,'please check login')
            return redirect('/')
        
    def post(self,request):
        total = 0
        current_user = request.user
        cart_item = ShopCart.objects.filter(user=current_user)
        if request.method == "POST":
            name = request.POST.get('name')
            email = request.POST.get('email')
            phone = request.POST.get('phone')
            country = request.POST.get('country')
            state = request.POST.get('state')
            city = request.POST.get('city')
            address = request.POST.get('address')
            selected_payment_method = request.POST.get('selectedPaymentMethod')
            
            
            grand_total = request.session.get('grand_total', 0) * 100
            requird_fields = [name,email,phone,country,state,city,address,selected_payment_method]
            if not all(requird_fields):
                messages.error(request,'Please fill in all the required fields.')
                return redirect('/order/checkout/')
            country_instance = Country.objects.get(name=country)
            state_instance = State.objects.get(name=state)
            city_instance = Town.objects.get(name=city)
            
            
            
            payment = Payment()
            payment.user = current_user
            payment.payment_method = selected_payment_method
            payment.amount_paid = grand_total
            
            order_details = Order()
            order_details.user = current_user
            order_details.payment = payment
            order_details.user_name = name
            order_details.email = email
            order_details.phone = phone
            order_details.address = address
            order_details.country = country_instance
            order_details.state = state_instance
            order_details.city = city_instance
            order_details.order_total = grand_total
            
            
            for item in cart_item:
                product_details = OrderProduct()
                product_details.order = order_details
                product_details.payment = payment
                product_details.user =current_user
                product_details.product = item.product
                product_details.quantity = item.quantity  
                item.product.quantity -= 1
                item.product.save()
                total += item.product.sale_price * item.quantity 
            tax = (2 * total) / 100    
            order_details.tax = tax    
                          
            
            if selected_payment_method == 'razorpay':
                client = razorpay.Client(auth=(settings.RAZORPAY_API_KEY, settings.RAZORPAY_API_SECRET))

                payment_data = {
                    "amount": grand_total,
                    "currency": "INR",
                    "receipt": "order_receipt",
                    "notes": {
                        "email": current_user.email,
                    },
                    }        
                order = client.order.create(data=payment_data)
                
                order_details.order_number = order["id"]
                payment.save()
                order_details.save()
                product_details.save()
                cart_item.delete()
                
                
                
                context={
                    'order_details':order_details,
                    'paymet_type':selected_payment_method,
                    'order':order
                }
                
                return render(request,'razorpay.html',context)
            elif selected_payment_method == 'cashondelivery':
                timestamp = int(time.time())
                random_chars = ''.join(random.choices('ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789', k=6))
                order_number = f'{timestamp}-{random_chars}'
                request.session['order_number'] = order_number
                order_details.order_number = order_number
                payment.save()
                order_details.save()
                product_details.save()
                ShopCart.objects.filter(user=current_user).delete()   
                return redirect('/order/payment_status/')    

            elif selected_payment_method == 'paypal':
                # Handle PayPal logic
                pass            
            

            
            
class PaymentStatus(View):
    def get(self,request):
        razorpay=request.GET.get('razorpay')
        if razorpay:
            response = request.POST
            razorpay_payment_id = response['razorpay_payment_id']
            try:
                order = Order.objects.get(order_number=response['razorpay_order_id'])
                order.payment.payment_id = razorpay_payment_id
                order.payment.save()
                return render(request,'order_complete.html',{'status':True})
            except:
                return render(request,'order_complete.html',{'status':False})  
        else:
            try:
                cod = 'cod'
                random_chars = ''.join(random.choices('ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789', k=6))
                payment_id = f'{cod}-{random_chars}'
                order_number = request.session.get('order_number')
                order = Order.objects.get(order_number=order_number)
                order.payment.payment_id = payment_id
                order.payment.save()
                return render(request,'order_complete.html',{'status':True})
            except:
                return render(request,'order_complete.html',{'status':False})             
                  
class ChangeQuantity(View):
    def post(self,request):
        current_user = request.user
        product_id = request.POST.get('product_id')
        action = request.POST.get('action')
        if request.user.is_authenticated:
            cart_item = get_object_or_404(ShopCart, user=request.user, product = product_id)
        else:
            cart = Cart.objects.get(cart_id=_cart_id(request))
            cart_item = get_object_or_404(ShopCart,cart_item=cart,product = product_id)


        if action == 'increment':
            if cart_item.quantity < cart_item.product.quantity:             
                cart_item.quantity += 1
            else:
                data = {
                    'status':"Requested quantity exceeds available quantity",
                    'new_quantity': cart_item.quantity,
                    'new_single_price': cart_item.product.sale_price * cart_item.quantity,    
                }  
                return JsonResponse(data)                
        elif action == 'decrement':
            if cart_item.quantity > 1:
                cart_item.quantity -= 1
            else:
                data = {
                    'status':"Zero quantity not allowed",
                    'new_quantity': cart_item.quantity,
                    'new_single_price': cart_item.product.sale_price * cart_item.quantity,    
                }  
                return JsonResponse(data)
        cart_item.single_price = cart_item.product.sale_price * cart_item.quantity
        cart_item.save()      
        
        data = {
            'status':"success",
            'new_quantity': cart_item.quantity,
            'new_single_price': cart_item.product.sale_price * cart_item.quantity,    
        }  
        return JsonResponse(data)

                    
        

            
            
            
            
            
            
            
            
            
            
                       