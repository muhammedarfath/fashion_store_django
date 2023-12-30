from django import forms
from shop.models import Variants
      
class AddVariant(forms.ModelForm):
    class Meta:
        model = Variants
        fields = [
            'product',
            'variant',
            'status',
        ]        