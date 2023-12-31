
from django.contrib import admin
from .models import Country, Order, OrderProduct, Payment, ShopCart, Cart, Town, Wishlist,State

# Customizing the display of Cart in the Django admin
class CartAdmin(admin.ModelAdmin):
    list_display = ['cart_id', 'date_added']

# Customizing the display of ShopCart in the Django admin
class ShopCartAdmin(admin.ModelAdmin):
    list_display = ['user', 'cart_item', 'product', 'quantity']

# Registering models with their corresponding custom admin classes
admin.site.register(Cart, CartAdmin)
admin.site.register(ShopCart, ShopCartAdmin)
admin.site.register(Wishlist)
admin.site.register(Country)
admin.site.register(State)
admin.site.register(Town)
admin.site.register(Order)
admin.site.register(OrderProduct)
admin.site.register(Payment)