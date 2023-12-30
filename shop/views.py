from django.http import HttpResponse
from django.shortcuts import render
from django.views import View
from shop.models import Product, Variants

# Create your views here.


# View to display all products
class ProductsShow(View):
    def get(self,request):
        products = Product.objects.all()
        context = {
            'products':products
        }
        return render(request,'shop.html',context)
 
 
 
# View to display a single product
class SingleProduct(View):
    def get(self,request,id):
        product = Product.objects.get(id=id)
        variants = Variants.objects.filter(product=product)

        productvariant = []

        selected_size_id = request.GET.get('size_id')

        for variant in variants:
            for related_product in variant.variant.all():
                productvariant.append(related_product)
                
        product_images = product.image_types.all()
        product_sizes = product.size.all()
          
        context = {
            'product':product,
            'variant':productvariant,
            'product_images':product_images,
            'product_sizes':product_sizes,
            'selected_size_id': selected_size_id,  
        }
        return render(request,'single_product.html',context)    