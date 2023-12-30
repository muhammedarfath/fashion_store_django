from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

#Custom signup form based on Django's UserCreationForm.
class SignupForm(UserCreationForm):

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')
