from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms
from django.core.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _

from users.models import Customer

class RegistrationForm(UserCreationForm):
    """this class handles the user registration form"""
    first_name = forms.CharField(max_length=30, required=True, help_text='Optional.')
    last_name = forms.CharField(max_length=30, required=True, help_text='Optional.')
    username = forms.CharField(max_length=30, required=True, help_text='Username.')
    email = forms.EmailField(max_length=254, help_text='Required. Inform a valid email address.')


    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'username', 'email', 'password1', 'password2'] #allowed fields

    def clean_email(self):
        """this function handles email cleaning"""
        email = self.cleaned_data['email']
        try:
            match = Customer.objects.get(email=email)
        except Customer.DoesNotExist:
            return email
        raise forms.ValidationError(_('The email already exists. Choose another'))