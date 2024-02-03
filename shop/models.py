from django.db import models
from autoslug import AutoSlugField
from django.contrib.auth.models import User


# Category model represents a product category.
class Category(models.Model):
    name = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return self.name

# Subcategory model represents a subcategory related to a specific category.
class Subcategory(models.Model):
    name = models.CharField(max_length=255)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='subcategories')

    def __str__(self):
        return self.name

# Color model represents a color option for a product.
class Color(models.Model):
    name = models.CharField(max_length=20)
    code = models.CharField(max_length=20, blank=True, null=True)
    
    def __str__(self):
        return self.name

# Size model represents a size option for a product.
class Size(models.Model):
    name = models.CharField(max_length=20)
    code = models.CharField(max_length=20, blank=True, null=True)

    def __str__(self):
        return self.name

# Images model represents images associated with a product.
class Images(models.Model):
    title = models.CharField(max_length=50, blank=True)
    image = models.ImageField(blank=True, upload_to="images/")

    def __str__(self):
        return self.title

# Product model represents a product with various attributes.
class Product(models.Model):
    STATUS = (
        ("True", "True"),
        ("False", "False"),
    )
    category = models.ForeignKey(Subcategory, on_delete=models.CASCADE)  
    title = models.CharField(max_length=150)
    keywords = models.CharField(max_length=255)
    description = models.TextField(max_length=255)
    image = models.ImageField(upload_to="images/", null=False)
    amount = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    sale_price = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    detail = models.TextField()
    quantity = models.IntegerField(default=1)
    slug = AutoSlugField(null=False, unique=True, populate_from='title')
    color = models.ForeignKey(Color, on_delete=models.CASCADE, blank=True, null=True)
    size = models.ManyToManyField(Size, blank=True)
    image_types = models.ManyToManyField(Images, blank=True)
    status = models.CharField(max_length=10, choices=STATUS)
    is_deleted = models.BooleanField(default=False)
    create_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title
    
# Variants model represents different variants/options for a product.
class Variants(models.Model):
    STATUS = (
        ("True", "True"),
        ("False", "False"),
    )
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    variant = models.ManyToManyField(Product, related_name='variant_products')
    status = models.CharField(max_length=10, choices=STATUS)

    
    def __str__(self):
        return self.product.title
    
# Product Comments     
class Comment(models.Model):
    STATUS = (
        ('New', 'New'),
        ('Read', 'Read'),
        ('Closed', 'Closed'),
    )
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    subject = models.CharField(max_length=50, blank=True)
    comment = models.CharField(max_length=250, blank=True)
    rate = models.IntegerField(default=1)
    status = models.CharField(max_length=10, choices=STATUS, default="New")
    create_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.subject
    