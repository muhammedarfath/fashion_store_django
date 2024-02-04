from django.http import HttpResponse, JsonResponse
from django.shortcuts import redirect, render
from django.views import View
from user.models import Payementwallet, UserProfile
from shop.models import Product
from home.models import ContactMessage, SliderImage
from django.contrib import messages
from django.db.models import Q
# Create your views here.

# Home view to render the main page
def home(request):
    userprofile = None

    if request.user.is_authenticated:
        userprofile = Payementwallet.objects.filter(user=request.user).first()


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
        'product':product,
        'userprofile':userprofile
        
        }
    return render(request,'index.html',context)


class Search(View):
    def get(self,request):
        search = request.GET.get('search')  
        pro_list = []

        if search:
            obj = Product.objects.filter(title__icontains=search)

            for i in obj:
                pro_list.append({
                    'title': i.title
                })

        return JsonResponse({
            'status': True,
            'pro_list': pro_list
        }) 
    def post(self,request):
        if request.method == 'POST':
            products=Product.objects.filter(status=True).order_by('id')
            search=request.POST.get('query')

            if search:
                products = products.filter(
                    Q(title__icontains=search)
                )
                
                context ={
                'products':products,
                }    
                return render(request,'search_product.html',context)
        else:
            return self.get(request)    
  
            
        
        


class Blog(View):
    def get(self,request):
        return render(request,'blog.html')
 
class AboutUs(View):
    def get(self,request):
        return render(request,'aboutus.html') 
    
class Contact(View):
    def get(self, request):
        return render(request, 'contact.html')   
    def post(self,request):
        try:
            if request.method == 'POST':
                name=request.POST['name']
                email=request.POST['email']
                message=request.POST['message']
                
                requird_fields = [name,email,message]
                if not all(requird_fields):
                    messages.error(request, 'Please fill in all the required fields.')
                    return redirect("/contact/")
                else:
                    data = ContactMessage()
                    data.name = name
                    data.email = email
                    data.message = message
                    data.save()
                    messages.success(request, "Your message has been sent. Thank you for your message.")
                    return redirect("/contact/")                       
            else:
                messages.error(request, "Please correct the errors below.")
                return render(request, 'contact.html')
                    
        except Exception as e:
            messages.error(request, "An error occurred while processing your message. Please try again.")
            return render(request, '404.html') 
                    

              
    
    
    
    
        


