from django.contrib import admin
from .models import ShopCart, Cart

# Customizing the display of Cart in the Django admin
class CartAdmin(admin.ModelAdmin):
    list_display = ['cart_id', 'date_added']

# Customizing the display of ShopCart in the Django admin
class ShopCartAdmin(admin.ModelAdmin):
    list_display = ['user', 'cart_item', 'product', 'quantity']

# Registering models with their corresponding custom admin classes
admin.site.register(Cart, CartAdmin)
admin.site.register(ShopCart, ShopCartAdmin)
