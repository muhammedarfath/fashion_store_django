from django.http import HttpResponse, HttpResponseNotFound
from django.shortcuts import get_object_or_404, redirect, render
from django.views import View
from order.models import OrderProduct
from shop.models import Comment, Product, Variants
from django.contrib import messages
from django.core.paginator import Paginator
# Create your views here.


# View to display all products
class ProductsShow(View):
    def get(self,request):
        catid = request.GET.get('categories')
        if catid:
            products = Product.objects.filter(category__id=catid, status=True).order_by("id")
            paginator = Paginator(products, 1)
            page = request.GET.get("page")
        else:    
            products = Product.objects.all()
            paginator = Paginator(products, 1)
            page = request.GET.get("page")     
        paged_product = paginator.get_page(page)      
        context = {
            'products':paged_product,
    
        }
        return render(request,'shop.html',context)
 
class SingleProduct(View):
    def get(self, request, id):
        try:
            product = get_object_or_404(Product, id=id)
        except (ValueError, Product.DoesNotExist):
            return HttpResponseNotFound("Product not found")

        current_user = request.user
        variants = Variants.objects.filter(product=product)

        productvariant = []

        selected_size_id = request.GET.get('size_id')

        for variant in variants:
            for related_product in variant.variant.all():
                productvariant.append(related_product)

        product_images = product.image_types.all()
        product_sizes = product.size.all()

        # Check if the user is authenticated before filtering OrderProduct
        if current_user.is_authenticated:
            orderproduct = OrderProduct.objects.filter(user=current_user, product=product).exists()
        else:
            orderproduct = None

        context = {
            'product': product,
            'variant': productvariant,
            'product_images': product_images,
            'product_sizes': product_sizes,
            'selected_size_id': selected_size_id,
            'orderproduct': orderproduct
        }
        return render(request, 'single_product.html', context)
 
class Review(View):
    def post(self,request,id):
        product = Product.objects.get(id=id)
        url = request.META.get('HTTP_REFERER')
        if request.method == 'POST': 
            sub = request.POST['subject']
            comment = request.POST['comment']
            data = Comment()
            data.subject = sub
            data.comment = comment
            data.product=product
            current_user= request.user
            data.user=current_user
            data.save() 
            messages.success(request, "Your review has ben sent. Thank you for your interest.")
            return redirect(url)
        return redirect(url)
                 
    
   