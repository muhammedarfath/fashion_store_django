from django.http import HttpResponse
from django.shortcuts import render
from django.views import View
from shop.models import Product, Variants

# Create your views here.

class ProductsShow(View):
    def get(self,request):
        products = Product.objects.all()
        context = {
            'products':products
        }
        return render(request,'shop.html',context)
    
class SingleProduct(View):
    def get(self,request,id):
        product = Product.objects.get(id=id)
        variants = Variants.objects.filter(product=product)

        productvariant = []
        

        for variant in variants:
            for related_product in variant.variant.all():
                productvariant.append(related_product)
                
        product_images = product.image_types.all()
  
        
        context = {
            'product':product,
            'variant':productvariant,
            'product_images':product_images
        }
        return render(request,'single_product.html',context)    