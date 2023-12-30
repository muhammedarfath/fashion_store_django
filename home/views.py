from django.http import HttpResponse
from django.shortcuts import render
from shop.models import Product
from home.models import SliderImage

# Create your views here.
def home(request):
    try:
        slider_instance = list(SliderImage.objects.filter(status=True))
        products_new_arrivals = Product.objects.filter(status = True).order_by("-create_at")[:2]
        products_best_sellers = Product.objects.filter(status=True).order_by("?")[:10]
    except SliderImage.DoesNotExist:
        slider_instance = []
  
    context = {
        'slider_instance':slider_instance,
        'products_new_arrivals':products_new_arrivals,
        'products_best_sellers':products_best_sellers
        }
    return render(request,'index.html',context)





