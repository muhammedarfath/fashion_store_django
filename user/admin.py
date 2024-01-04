from django.contrib import admin

from .models import Coupon, Payementwallet, UserProfile

# Register your models here.

admin.site.register(Payementwallet)
admin.site.register(UserProfile)
admin.site.register(Coupon)