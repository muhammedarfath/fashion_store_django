from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.views import View
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from order.models import Order, OrderProduct
from user.models import Coupon
from shop.models import Color, Images, Product, Size, Subcategory, Variants
from .forms import AddVariant 
from django.contrib import messages
from django.views.decorators.cache import never_cache
from django.utils.decorators import method_decorator
from django.contrib.auth import authenticate,login,logout



@method_decorator(never_cache, name='dispatch')  
class AdminLogin(View):
    def get(self,request):
        if request.user.is_authenticated and request.user.is_superuser:
            return redirect('/adminpanel/dashboard/')
        else:
            return render(request,'admin_login.html')
    def post(self,request):    
        if request.method =='POST':
            username=request.POST['username']
            password=request.POST['password']
            
            if username.strip()=='' or password.strip()=='':
                messages.error(request,'fields cannot be empty')
            else:
                user=authenticate(username=username,password=password)
                
                if user and user.is_superuser:
                    login(request,user)
                    return redirect('/adminpanel/dashboard/')
                else:
                    messages.error(request ,'Invalid username or password')
                    return redirect('/adminpanel/admin_login/')
        else:
            return render(request,'admin_login.html')



@method_decorator(never_cache, name='dispatch')  
class DashBoard(View):
    def get(self, request):
        if request.user.is_authenticated and request.user.is_superuser:
                users = User.objects.filter(is_superuser=True)
                return render(request, 'dashboard.html')
        else:
            return redirect('/adminpanel/admin_login/') 
 
 
  
class UserList(View):
    def get(self,request):
        if request.user.is_authenticated and request.user.is_superuser:
            user = User.objects.all()
            context = {
                'user':user
            }
            return render(request,'user_list.html',context)    
        else:
            return redirect('/adminpanel/admin_login/')   
  
  
    
class ProductList(View):
    def get(self,request):
        if request.user.is_authenticated and request.user.is_superuser:
            product = Product.objects.all()
            context = {
                'product':product
            }
            return render(request,'product_list.html',context)  
        else:
            return redirect('/adminpanel/admin_login/')   
  
    
    
class ProductAdd(View):
    template_name = 'product_add.html'

    def get(self, request):
        if request.user.is_authenticated and request.user.is_superuser:        
            color = Color.objects.all()
            size = Size.objects.all()
            category = Subcategory.objects.all()
            product = Product.objects.all()
            context = {
                'color': color,
                'size': size,
                'category': category,
                'product_status': Product.STATUS,
                'product': product,
                'variant_status': Variants.STATUS
            }
            return render(request, self.template_name, context)
        else:
            return redirect('/adminpanel/admin_login/')   
        
    def post(self, request):
        category = request.POST.get('category')
        title = request.POST.get('title')
        description = request.POST.get('description')
        image = request.FILES.get('image')
        amount = request.POST.get('amount')
        sale_price = request.POST.get('sale_price')
        detail = request.POST.get('detail')
        quantity = request.POST.get('quantity')
        color = request.POST.get('color')
        sizes = request.POST.getlist('size')
        image_types = request.FILES.getlist('image_types')
        status = request.POST.get('status')

        required_fields = [category, title, description, image, amount, sale_price, detail, quantity, color, sizes, image_types, status]
        
        if not all(required_fields):
            messages.error(request, 'Please fill in all the required fields.')
            return redirect('/adminpanel/productadd/')

        existing_product = Product.objects.filter(
            title=title,
            category=category,
            image=image,
        )

        if existing_product.exists():
            messages.error(request, 'Similar product already exists')
            return redirect('/adminpanel/productadd/')

        # Create Image objects for each image type
        image_type_objects = [Images.objects.create(image=img_type) for img_type in image_types]

        # Get instances of related models
        category_instance = Subcategory.objects.get(id=category)
        color_instance = Color.objects.get(name=color)
        size_instances = Size.objects.filter(name__in=sizes)

        # Create the Product instance
        product = Product.objects.create(
            category=category_instance,
            title=title,
            description=description,
            image=image,
            amount=amount,
            sale_price=sale_price,
            detail=detail,
            quantity=quantity,
            color=color_instance,
            status=status
        )

        # Add size_instances to the product
        product.size.set(size_instances)

        # Add image types to the product
        product.image_types.set(image_type_objects)

        messages.success(request, 'Product added')
        return redirect('/adminpanel/productlist/')
    
    
    
    
class EditProduct(View):
    def get(self,request, id):
        if request.user.is_authenticated and request.user.is_superuser:
            product = get_object_or_404(Product, id=id)
            variant = Variants.objects.get(product=product)
            category = Subcategory.objects.all()
            color = Color.objects.all()
            size = Size.objects.all()
            
            context={
                'product_status': Product.STATUS,
                'color':color,
                'size':size,
                'product':product,
                'category':category,
                'variant':variant,
                'variant_status': variant.STATUS
            }
            return render(request, 'edit_product.html', context)
        else:
            return redirect('/admin_login/')
    def post(self, request,id):
            product = get_object_or_404(Product, id=id)
            category = request.POST.get('category')
            title = request.POST.get('title')
            description = request.POST.get('description')
            image = request.FILES.get('image')
            amount = request.POST.get('amount')
            sale_price = request.POST.get('sale_price')
            detail = request.POST.get('detail')
            quantity = request.POST.get('quantity')
            color = request.POST.get('color')
            sizes = request.POST.getlist('size')
            image_types = request.FILES.getlist('image_types')
            status = request.POST.get('status')
            if image_types:
               image_type_objects = [Images.objects.create(image=img_type) for img_type in image_types]
               product.image_types.set(image_type_objects)
            
            category_instance = Subcategory.objects.get(id=category)
            color_instance = Color.objects.get(id=color)
            size_instances = Size.objects.filter(name__in=sizes)
            
            
            
            product.category=category_instance
            product.title=title
            product.description=description
            if image != None:
               product.image=image
            product.amount=amount
            product.sale_price=sale_price
            product.detail=detail
            product.quantity=quantity
            product.color=color_instance
            product.status=status
            
            
            # Add size_instances to the product
            product.size.set(size_instances)


            product.save()
            messages.success(request, 'Edit Successfully')
            return redirect('/adminpanel/productlist/')              
            
    
    
      
        
class AddVariant(View):   
    form_class = AddVariant 
    def get(self,request):
        if request.user.is_authenticated and request.user.is_superuser:        
            return render(request,'product_list.html')  
        else:
            return redirect('/adminpanel/admin_login/')            
    def post(self,request):
        form = self.form_class(request.POST, request.FILES)
        if form.is_valid():
            form.save()  
            return redirect('/adminpanel/productlist/')     
        else:
            return HttpResponse(form.errors)
            
        
        
class Couponshow(View):
    template_name = "admincoupon.html"

    def get(self, request):
        coupons = Coupon.objects.all()
        context = {
            "coupons": coupons
        }
        return render(request, self.template_name, context)
    
    
class AddCoupon(View):
    template_name = "addcoupon.html"
    def get(self, request):
        if request.user.is_authenticated and request.user.is_superuser:
            return render(request, self.template_name)       
        else:   
            return redirect('/adminpanel/admin_login/') 
    def post(self, request):
        if request.method == "POST":
            coupon_name = request.POST.get('coupon_name')
            coupon_code = request.POST.get('coupon_code')
            coupon_image = request.FILES.get('coupon_image')  # Handle file upload
            coupon_discount = request.POST.get('coupon_discount')
            coupon_minimum_amount = request.POST.get('coupon_minimum_amount')
            coupon_expiration_time = request.POST.get('coupon_expiration_time')
            

            # Create and save the Coupon object
            coupon = Coupon(
                user=request.user,  # Assuming you have a logged-in user
                offer_name=coupon_name,
                code=coupon_code,
                image=coupon_image,
                discount_price=coupon_discount,
                minimum_amount=coupon_minimum_amount,
                expiration_time=coupon_expiration_time,
            )
            coupon.save()
            return redirect('/adminpanel/coupon/')  
    
    
class SoftDeleteCoupon(View):
    def get(self,request,id):
        if request.user.is_authenticated and request.user.is_superuser:
            coupon = get_object_or_404(Coupon, pk=id)
            if coupon.active:
                coupon.active = False
            else:
                coupon.active = True    
            coupon.save()
            return redirect('/adminpanel/coupon/') 
        else:
            return redirect('/adminpanel/admin_login/')    
     
                    
class EditCoupon(View):
    template_name = "edit_coupon.html"

    def get(self, request, id):
        if request.user.is_authenticated and request.user.is_superuser:
            coupon = get_object_or_404(Coupon, id=id)
            context = {"coupon": coupon}
            return render(request, self.template_name, context)
        else:
            return redirect('/adminpanel/admin_login/')  

    def post(self, request, id):
        coupon = get_object_or_404(Coupon, id=id)

        # Retrieve form data
        coupon_name = request.POST.get('coupon_name')
        discount = request.POST.get('coupon_discount')
        minimum_amount = request.POST.get('coupon_minimum_amount')
        coupon_expiration_time = request.POST.get('coupon_expiration_time')
        image = request.FILES.get('coupon_image')

        # Update Coupon instance
        coupon.offer_name = coupon_name
        coupon.discount_price = discount
        coupon.minimum_amount = minimum_amount

        # Handle expiration time format conversion
        if coupon_expiration_time:
            coupon.expiration_time = coupon_expiration_time

        if image:
            coupon.image = image

        coupon.save()
        messages.success(request, 'Coupon edited successfully')

        return redirect('/adminpanel/coupon/')
    
    
    
    
class Orders(View):
    def get(self,request):
        orders = OrderProduct.objects.all().order_by('-create_at')
        context = {
            'orders': orders,
        }
        return render(request, 'orders_list.html', context) 
    
    
    
class OrderDetails(View):
    def get(self,request,id):
        orders = OrderProduct.objects.get(id=id)
        context = {
            'order_status':Order.ORDERSTATUS,
            'orders': orders,
        }        
        return render(request,'order_details.html',context)
    def post(self,request,id):
        url = request.META.get('HTTP_REFERER')
        if request.method == 'POST':
            selected_status = request.POST.get('orderStatus', None)
            selected_order_id = request.POST['orderId']
            if selected_status is not None:
                orders = OrderProduct.objects.get(order=selected_order_id)
                orders.order.status = selected_status
                orders.order.save()
                return redirect(url)
            else:
                return redirect(url)



# def refund(request, id):
#     url = request.META.get('HTTP_REFERER')
#     order_product = OrderProduct.objects.get(id=id)
#     user_wallet = UserProfile.objects.get(user=order_product.order.user)
#     if order_product.status == 'Canceled':
#         order_product.order.status = 6
#     else:
#         order_product.order.status = 7 
        
#     if order_product.order.coupon:
#         total = order_product.order.order_total - order_product.order.coupon.discount_price
#         user_wallet.wallet += Decimal(str(total))
#     else:
#         user_wallet.wallet += Decimal(str(order_product.order.order_total))
    
#     wallet_details = Payementwallet(user=order_product.order.user)
#     wallet_details.paymenttype = "Credit"
#     wallet_details.wallet = Decimal(str(order_product.order.order_total))
#     mail_subject = "Your refund has been successfully approved."
#     message = render_to_string(
#             "refund_recieved_email.html", {"user": order_product.order.user, "wallet": order_product.order.order_total}
#         )
#     to_email = order_product.order.user.email
#     send_mail = EmailMessage(mail_subject, message, to=[to_email])
#     send_mail.send()
    
#     wallet_details.save()
#     user_wallet.save()
#     order_product.order.save()
#     return HttpResponseRedirect(url)
  
    

