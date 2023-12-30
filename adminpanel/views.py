from django.http import HttpResponse
from django.shortcuts import redirect, render
from django.views import View
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from shop.models import Color, Images, Product, Size, Subcategory, Variants
from .forms import AddVariant 
from django.contrib import messages

# Create your views here.
class DashBoard(View):
    # @login_required
    def get(self, request):
        return render(request, 'dashboard.html')
    
class UserList(View):
    def get(self,request):
        user = User.objects.all()
        context = {
            'user':user
        }
        return render(request,'user_list.html',context)    
    
class ProductList(View):
    def get(self,request):
        product = Product.objects.all()
        context = {
            'product':product
        }
        return render(request,'product_list.html',context)  
    
    
class ProductAdd(View):
    def get(self,request):
        color = Color.objects.all()
        size = Size.objects.all()
        category = Subcategory.objects.all()
        product = Product.objects.all()
        context = {
            'color':color,
            'size':size,
            'category':category,
            'product_status':Product.STATUS,
            'product':product,
            'variant_status':Variants.STATUS
        }
        return render(request,'product_add.html',context)  
    def post(self, request):
        if request.method == 'POST':
            category = request.POST.get('category')
            title = request.POST.get('title')
            description = request.POST.get('description')
            image = request.FILES.get('image')
            amount = request.POST.get('amount')
            sale_price = request.POST.get('sale_price')
            detail = request.POST.get('detail')
            quantity = request.POST.get('quantity')
            color = request.POST.get('color')
            size = request.POST.get('size')
            image_types = request.FILES.getlist('image_types')
            status = request.POST.get('status')
            
            required_fields = [category, title, description, image, amount, sale_price,detail,quantity,color,size,image_types,status]
            existing_product = Product.objects.filter(
                title=title,
                category=category,
                image=image, 
            )
            if not all(required_fields):
                messages.error(request, 'Please fill in all the required fields.')
                return redirect('/adminpanel/productadd/')
            elif existing_product.exists():
                messages.error(request,'similar product already exists')
                return redirect('/adminpanel/productadd/')
            else:
                # Create Image objects for each image type
                image_type_objects = []
                if image_types:
                    for img_type in image_types:
                        image_type_obj = Images.objects.create(image=img_type)
                        image_type_objects.append(image_type_obj)

                # Get instances of related models
                category_instance = Subcategory.objects.get(id=category)
                color_instance = Color.objects.get(name=color)
                size_instance = Size.objects.get(name=size)

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
                    size=size_instance,
                    status=status
                )

                # Add image types to the product
                product.image_types.set(image_type_objects)
                product.save()
                messages.success(request,'product added')
                return redirect('/adminpanel/productlist/')
        else:
            return self.get(request)
        
        
        
class AddVariant(View):   
    form_class = AddVariant 
    def get(self,request):
        return render(request,'product_list.html')   
    def post(self,request):
        form = self.form_class(request.POST, request.FILES)
        if form.is_valid():
            form.save()  
            return redirect('/adminpanel/productlist/')     
        else:
            return HttpResponse(form.errors)
            
        

            
    
