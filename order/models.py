from django.db import models
from django.contrib.auth.models import User
from shop.models import Product
# Create your models here.


# Cart model represents a shopping cart identified by a cart_id.
class Cart(models.Model):
    cart_id = models.CharField(max_length=250, blank=True)
    date_added = models.DateField(auto_now_add=True)


# ShopCart model represents items added to the shopping cart.
class ShopCart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    cart_item = models.ForeignKey(Cart, on_delete=models.CASCADE, null=True, default=None)
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True)
    quantity = models.IntegerField()
    
    def __str__(self):
        if self.user:
            return f"Cart for {self.user.username}"
        else:
            return "Cart for unknown user"
    