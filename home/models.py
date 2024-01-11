from django.db import models
from shop.models import Images
# Create your models here.

# SliderImage model represents images for a slider with status (True/False).
class SliderImage(models.Model):
    STATUS = (
        ('True', 'True'),
        ('False', 'False'),
    )
    image = models.ImageField(blank=True,upload_to='images/')
    status=models.CharField(max_length=10,choices=STATUS)
    create_at=models.DateTimeField(auto_now_add=True)
    update_at=models.DateTimeField(auto_now=True)
    
    

# Settings model represents various settings for the website.
class Settings(models.Model):
    STATUS = (
            ('True', 'True'),
            ('False', 'False'),
    )
    title = models.CharField(max_length=150)
    keywords = models.CharField(max_length=255)
    description = models.CharField(max_length=255)
    company = models.CharField(max_length=50)
    address = models.CharField(blank=True,max_length=100)
    phone = models.CharField(blank=True,max_length=15)
    email = models.CharField(blank=True,max_length=50)
    icon = models.ImageField(blank=True,upload_to='images/')
    facebook = models.CharField(blank=True,max_length=50)
    instagram = models.CharField(blank=True,max_length=50)
    twitter = models.CharField(blank=True,max_length=50)
    youtube = models.CharField(blank=True, max_length=50)
    aboutus = models.TextField(blank=True)
    contact = models.TextField(blank=True)
    status=models.CharField(max_length=10,choices=STATUS)
    create_at=models.DateTimeField(auto_now_add=True)
    update_at=models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title
    
    
class Banners(models.Model):
    STATUS = (
        ('True', 'True'),
        ('False', 'False'),
    )
    discount_banner = models.ManyToManyField(Images, blank=True)
    product_banner = models.ImageField(blank=True,upload_to='images/')
    aboutus_banner = models.ImageField(blank=True,upload_to='images/')
    contact_banner = models.ImageField(blank=True,upload_to='images/')
    blog_banner = models.ManyToManyField(Images, blank=True, related_name='blog_banners')
    status=models.CharField(max_length=10,choices=STATUS)
    create_at=models.DateTimeField(auto_now_add=True)
    update_at=models.DateTimeField(auto_now=True)
        
        
        
class ContactMessage(models.Model):
    STATUS = (
        ('New', 'New'),
        ('Read', 'Read'),
        ('Closed', 'Closed'),
    )
    name= models.CharField(blank=True,max_length=20)
    email= models.CharField(blank=True,max_length=50)
    message= models.TextField(blank=True,max_length=255)
    status=models.CharField(max_length=10,choices=STATUS,default='New')
    note = models.CharField(blank=True, max_length=100)
    create_at=models.DateTimeField(auto_now_add=True)
    update_at=models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name        