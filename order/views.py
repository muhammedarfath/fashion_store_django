from django.utils import timezone
from django.http import HttpResponse, JsonResponse
from django.shortcuts import redirect, render ,get_object_or_404
from django.views import View
from user.models import Coupon, UserProfile
from shop.models import Product, Size
from order.models import Cart, Country, Order, OrderProduct, Payment, ShopCart, State, Town, Wishlist
from django.contrib import messages
from django.core.exceptions import ObjectDoesNotExist
import razorpay
import random
import time
from django.conf import settings



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
            coupon = Coupon.objects.filter(is_expired = False)
            for co in coupon:
                if cart_item in coupon:
                    return HttpResponse("true")
               
            request.session['grand_total'] = float(grand_total)
            
            context = {
                'cart_item':cart_item,
                'grand_total':grand_total,
                'tax':tax,
                'total':self.total
            }                
                
        except ObjectDoesNotExist:
            pass
        return render(request,'cart.html',context)
        
    def post(self,request):
        if request.method == "POST":
            user = request.user
            cart_items = ShopCart.objects.filter(user=user)
            for item in cart_items:
                self.total += item.single_price
            tax = (2 * self.total) / 100
            grand_total = self.total + tax
            coupon_code = request.POST.get('couponcode')
            coupon = Coupon.objects.filter(code=coupon_code,active=True).first()
            if coupon:
                current_time = timezone.now()
                if current_time <= coupon.expiration_time and coupon.is_one_time_use == False and coupon.minimum_amount <= self.total:
                    discount_amount = self.total - coupon.discount_price
                    grand_total = discount_amount + tax
                    
                    request.session['discount'] = coupon.discount_price
                    request.session['offername'] = coupon.offer_name
                    
                    response_data = {
                        'coupon': coupon.discount_price,
                        'tax': tax,
                        'grand_total': grand_total,
                        'success': f"Coupon '{coupon.offer_name}' applied successfully! You saved ₹{coupon.discount_price:.2f}",
                    }            
                    return JsonResponse(response_data)                    
                else:
                    return JsonResponse({'error': 'Invalid coupon ,check expire date and minimun amount'})   

        

  
# View for adding a product to the shopping cart  
class AddToCart(View): 
    def post(self,request,id):
        url = request.META.get("HTTP_REFERER")
        current_user = request.user
        size_id = request.GET.get('size_id') 
    
        if size_id:
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
                    cart_item = ShopCart.objects.filter(cart_item=cart,product=product,size=size_instance).first()
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
        else:
            messages.error(request,'please select size')  
            return redirect(url)      




        
#change quantity                       
class ChangeQuantity(View):
    def post(self, request):
        current_user = request.user
        product_id = request.POST.get('product_id')
        action = request.POST.get('action')
        size = request.POST.get('size')
        response_data = {}

        if current_user.is_authenticated:
            cart_item = get_object_or_404(ShopCart, user=current_user, id=product_id, size=size)

        else:
            cart = Cart.objects.get(cart_id=_cart_id(request))
            cart_item = get_object_or_404(ShopCart, cart_item=cart, id=product_id, size=size)

        if action == 'increment':
            if cart_item.quantity < cart_item.product.quantity:
                cart_item.quantity += 1
            else:
                response_data['status'] = "Requested quantity exceeds available quantity"
        elif action == 'decrement':
            if cart_item.quantity > 1:
                cart_item.quantity -= 1
            else:
                response_data['status'] = "Zero quantity not allowed"

        cart_item.single_price = cart_item.product.sale_price * cart_item.quantity
        cart_item.save()

        cart_items = ShopCart.objects.filter(user=current_user) if current_user.is_authenticated else ShopCart.objects.filter(cart_item=cart)
        total = sum(cart_item.product.sale_price * cart_item.quantity for cart_item in cart_items)

        tax = (2 * total) / 100
        grand_total = tax + total
        
        response_data.update({
            'new_quantity': cart_item.quantity,
            'new_single_price': cart_item.product.sale_price * cart_item.quantity,
            'tax': tax,
            'grand_total': grand_total,
            'total':total
        })

        return JsonResponse(response_data)
            




#Remove product from cart 
class RemoveCart(View):
    def get(self,request,id):
        if request.user.is_authenticated:
            cart_item = ShopCart.objects.get(user=request.user,id=id)
        else:
            cart = Cart.objects.get(cart_id=_cart_id(request))    
            cart_item = ShopCart.objects.filter(cart_item=cart,id=id)  

        cart_item.delete()
        messages.success(request,'item removed form cart')
        return redirect('/order/shopcart/')
            


#The product wishlist is only visible after logging in.            
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
                


#add to wishlist 
class AddToWishList(View):
    def get(self, request, id):
        current_user = request.user
        if current_user.is_authenticated:
            product = get_object_or_404(Product, id=id)
            
            size_id = request.GET.get('size_id', None)
            if size_id:
                size = Size.objects.get(id=size_id)
                if size and product.size.filter(name=size.name).exists():
                    wishlist_item = Wishlist.objects.filter(user=current_user, product=product, size=size.name)
                    cart_item = ShopCart.objects.filter(user=current_user, product=product)
                    
                    if wishlist_item.exists():
                        messages.success(request, 'This item is already added to the wishlist')
                        return redirect('/order/wishlist/')
                    elif cart_item.exists():
                        messages.success(request, 'This item is already added to the cart')
                        return redirect('/order/shopcart/')
                    else:
                        Wishlist.objects.create(user=current_user, product=product, size=size.name)
                        messages.success(request, 'Item added to wishlist')
                        return redirect('/order/wishlist/')
                else:
                    messages.warning(request, 'Invalid size or size not provided')
                    return redirect('/')
            else:
                messages.warning(request,'please select the size') 
                return redirect(f'/shop/singleproduct/{id}/')       
        else:
            messages.warning(request, 'Please login')
            return redirect('/')
          
  
  
  
#product checkout enter details   
class CheckOut(View):
    def get(self,request):
        current_user = request.user
        if current_user.is_authenticated:
            cart_item = ShopCart.objects.filter(user=current_user)
            userprofile = UserProfile.objects.filter(user=current_user).first()
            if  cart_item:
                if userprofile:
                    grand_total = (request.session.get('grand_total', 0) - request.session.get('discount', 0)) 
                    countries = Country.objects.all()
                    states = State.objects.all()
                    city = Town.objects.all()
                    context = {
                        'countries':countries,
                        'states':states,
                        'city':city,
                        'cart_item':cart_item,
                        'grand_total':grand_total,
                        'userprofile': userprofile,
                    }
                    return render(request,'checkout.html',context)  
                else:
                    messages.error(request,'please create your profile')
                    return redirect('/user/account/')                        
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
            
            coupon = request.session.get('discount', 0)
            grand_total = (request.session.get('grand_total', 0) - request.session.get('discount', 0)) 
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
            if coupon:
                offer_name=request.session.get('offername')
                coupon = Coupon.objects.get(offer_name=offer_name)
                order_details.coupon = coupon
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
                grand_total = (request.session.get('grand_total', 0) - request.session.get('discount', 0)) * 100
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
            

  
            
#payment status 'cod and razorpay'           
class PaymentStatus(View):
    def get(self,request):
        try:
            cod = 'cod'
            random_chars = ''.join(random.choices('ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789', k=6))
            payment_id = f'{cod}-{random_chars}'
            order_number = request.session.get('order_number')
            order = Order.objects.get(order_number=order_number)
            order.payment.payment_id = payment_id
            order.payment.save()
            context = {
                'status':True,
                'order':order,
            }
            return render(request,'order_complete.html',context)
        except:
            return render(request,'order_complete.html',{'status':False}) 
        
    def post(self, request):
        razorpay_get = request.GET.get('razorpay')
        razorpay_post = request.POST.get('razorpay')
        
        razorpay = razorpay_get or razorpay_post
        if razorpay:
            response = request.POST
            print(response)
            razorpay_payment_id = response.get('razorpay_payment_id')
            print(razorpay_payment_id)
            try:
                order = Order.objects.get(order_number=response.get('razorpay_order_id'))
                order.payment.payment_id = razorpay_payment_id
                order.payment.save()
                orderproduct = OrderProduct.objects.filter(order=order)
                context = {
                    'order':order,
                    'orderproduct':orderproduct
                }
                
                return render(request,'order_complete.html',context)
            except Order.DoesNotExist:
                return render(request, 'order_complete.html', {'status': False, 'message': 'Order not found'})
            except Exception as e:
                print(e)  # Log the specific exception for debugging
                return render(request, 'order_complete.html', {'status': False, 'message': 'An error occurred'})
        else:
            return render(request, 'razorpay.html')
        
        
            

            
            
            
            
            
            
                       