from django.http import HttpResponse
from django.shortcuts import redirect, render
from django.views import View
from home.forms import ContactForm
from shop.models import Product
from home.models import SliderImage
from django.contrib import messages

# Create your views here.

# Home view to render the main page
def home(request):
    try:
        slider_instance = list(SliderImage.objects.filter(status=True))
        products_new_arrivals = Product.objects.filter(status = True).order_by("-create_at")[:2]
        products_best_sellers = Product.objects.filter(status=True).order_by("?")[:10]
        product = Product.objects.all().order_by("?")
    except SliderImage.DoesNotExist:
        slider_instance = []
  
    context = {
        'slider_instance':slider_instance,
        'products_new_arrivals':products_new_arrivals,
        'products_best_sellers':products_best_sellers,
        'product':product
        }
    return render(request,'index.html',context)


class Blog(View):
    def get(self,request):
        return render(request,'blog.html')
 
class AboutUs(View):
    def get(self,request):
        return render(request,'aboutus.html') 
    
class Contact(View):
    def get(self,request):
        return render(request,'contact.html')     
    def post(self,request):
        try:
            if request.method == 'POST':
                form = ContactForm(request.POST)
                if form.is_valid():
                    form.save()
                    messages.success(request, "Your message has ben sent. Thank you for your message.")
                    return redirect("/contact/")
                else:
                    messages.error(request, "Please correct the errors below.")
                    return render(request, 'contact.html', {'form': form})
                    
        except Exception as e:
            messages.error(request, "An error occurred while processing your message. Please try again.")
            return render(request, '404.html') 
                    
    
                
    
    
    
    
        


