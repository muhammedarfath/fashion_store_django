from django.contrib import admin
from .models import *

# Customizing the display of Category in the Django admin
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name']

# Customizing the display of Subcategory in the Django admin
class SubcategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'category']

# Customizing the display of Product in the Django admin
class ProductAdmin(admin.ModelAdmin):
    list_display = ['title', 'category', 'amount', 'status', 'create_at']
    list_filter = ['status', 'create_at']
    search_fields = ['title', 'description']

# Customizing the display of Color in the Django admin
class ColorAdmin(admin.ModelAdmin):
    list_display = ['name', 'code']

# Customizing the display of Size in the Django admin
class SizeAdmin(admin.ModelAdmin):
    list_display = ['name', 'code']

# Customizing the display of Images in the Django admin
class ImagesAdmin(admin.ModelAdmin):
    list_display = ['title', 'image']

# Customizing the display of Variants in the Django admin
class VariantsAdmin(admin.ModelAdmin):
    list_display = ['product', 'status']

# Registering models with their corresponding custom admin classes
admin.site.register(Category, CategoryAdmin)
admin.site.register(Subcategory, SubcategoryAdmin)
admin.site.register(Product, ProductAdmin)
admin.site.register(Color, ColorAdmin)
admin.site.register(Size, SizeAdmin)
admin.site.register(Images, ImagesAdmin)
admin.site.register(Variants, VariantsAdmin)
admin.site.register(Comment)
