from .models import Banners, ContactMessage, SliderImage, Settings
from django.contrib import admin

# Registering models for admin management
admin.site.register(SliderImage)
admin.site.register(Settings)
admin.site.register(Banners)
admin.site.register(ContactMessage)
