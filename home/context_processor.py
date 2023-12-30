from order.models import Cart, ShopCart
from order.views import _cart_id
from shop.models import Subcategory
from .models import Banners, Settings
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.models import AnonymousUser
# Context processor to provide footer data to all templates
def footer_data(request):
    """
    Retrieve the Settings instance with status=True to provide footer data.

    Args:
        request: Django HttpRequest object.

    Returns:
        Dictionary containing the 'footer_data' key with the Settings instance.
    """
    try:
        settings_instance = Settings.objects.get(status=True)
        
    except Settings.DoesNotExist:
        # If not found, set settings_instance to None
        settings_instance = None

    # Return a dictionary with the 'footer_data' key and the Settings instance
    return {'footer_data': settings_instance}


def header_data(request):
    try:
        menu_bar = Subcategory.objects.all()
    except Subcategory.DoesNotExist:
        menu_bar = None    
        
    return {'header_data':menu_bar}   



def banners_images(request):
    try:
        banners = Banners.objects.all()
    except Banners.DoesNotExist:
        banners = None    
        
    return {'banners_images':banners}    


def shopcart_details(request):
    shopcart = None 
    try:
        current_user = request.user
        if isinstance(current_user, AnonymousUser):
            cart = Cart.objects.get(cart_id=_cart_id(request))
            shopcart = ShopCart.objects.filter(cart_item=cart)
        else:
            shopcart = ShopCart.objects.filter(user=current_user)
    except ObjectDoesNotExist:
        pass

    return {'shopcart_details': shopcart}