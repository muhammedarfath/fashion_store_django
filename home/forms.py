
from django.forms import ModelForm
from home.models import ContactMessage


class ContactForm(ModelForm):
    class Meta:
        model = ContactMessage
        fields = ('name', 'email', 'message')