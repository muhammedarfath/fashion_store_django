from django.db import models
from django.contrib.auth.models import User
from user.models import Coupon
from shop.models import Product, Size
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
    size = models.CharField(max_length=20,null=True)
    single_price = models.FloatField(blank=True, null=True)
    order_total = models.FloatField(blank=True, null=True)


    def __str__(self):
        if self.user:
            return f"Cart for {self.user.username}"
        else:
            return "Cart for unknown user"

# Wishlist model represents items added to the user's wishlist.
class Wishlist(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True)
    size = models.CharField(max_length=20,null=True)
    added_at = models.DateTimeField(auto_now_add=True)
    quantity = models.IntegerField(null=True, default=1)
    

    def __str__(self):
        return f"{self.user.username}'s Wishlist"
     
# Country model represents a country.      
class Country(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

# State model represents a state within a country.
class State(models.Model):
    name = models.CharField(max_length=100)
    country = models.ForeignKey(Country, on_delete=models.CASCADE)

    def __str__(self):
        return self.name

# Town model represents a town within a state.
class Town(models.Model):
    name = models.CharField(max_length=100)
    state = models.ForeignKey(State, on_delete=models.CASCADE)

    def __str__(self):
        return self.name    
       
# Payment model represents a payment made by a user.
class Payment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    payment_id = models.CharField(max_length=100)
    payment_method = models.CharField(max_length=100)
    amount_paid = models.CharField(max_length=100)
    status = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return self.payment_id

# Order model represents an order placed by a user.
class Order(models.Model):
    ORDERSTATUS = (
    ("New", "New"),
    ("Accepted", "Accepted"),
    ("Preparing", "Preparing"),
    ("OnShipping", "OnShipping"),
    ("Completed", "Completed"),
    ("Canceled", "Canceled"),
    ("Return", "Return"),
    )
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    payment = models.ForeignKey(Payment, on_delete=models.CASCADE, blank=True, null=True)
    order_number = models.CharField(max_length=20, blank=True, null=True)
    user_name = models.CharField(max_length=100)
    email = models.CharField(max_length=30, null=True, blank=True)
    phone = models.CharField(blank=True, max_length=20)
    address = models.CharField(max_length=100, blank=True, null=True)
    country = models.ForeignKey(Country, on_delete=models.CASCADE, null=True)
    city = models.ForeignKey(Town, on_delete=models.CASCADE, null=True)
    state = models.ForeignKey(State, on_delete=models.CASCADE, null=True)
    order_total = models.FloatField(blank=True, null=True)
    tax = models.FloatField(blank=True, null=True)
    user_note = models.CharField(blank=True, max_length=100)
    coupon = models.ForeignKey(Coupon, on_delete=models.SET_NULL, null=True, blank=True)
    status = models.CharField(max_length=10,choices=ORDERSTATUS, default="New",blank=True,null=True)
    create_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.user_name

# OrderProduct model represents products within an order.
class OrderProduct(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    payment = models.ForeignKey(Payment, on_delete=models.CASCADE, blank=True, null=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField()
    create_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)


    