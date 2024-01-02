from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class Payementwallet(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    paymenttype=models.CharField(max_length=150,blank=True,null=True)
    wallet = models.DecimalField(default=0, decimal_places=2, max_digits=10,null=True,blank=True)
    created = models.DateField(auto_now_add=True)

    def __str__(self):
        return f"PaymentWallet for User: {self.user}, Payment Type: {self.paymenttype}, Created on: {self.created}"


class UserProfile(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    phone = models.CharField(blank=True, max_length=20)
    address = models.CharField(blank=True, max_length=150)
    city = models.CharField(blank=True, max_length=100)
    state = models.CharField(blank=True, max_length=50,null=True)
    country = models.CharField(blank=True, max_length=50)
    image = models.ImageField(blank=True, upload_to='images/users/')
    # wallet = models.ForeignKey(Payementwallet, on_delete=models.CASCADE,null=True)

    def __str__(self):
        return self.user.username

    




