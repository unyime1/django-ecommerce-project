from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms
from django.core.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _

from users.models import Customer

class RegistrationForm(UserCreationForm):
    """this class handles the user registration form"""
    first_name = forms.CharField(max_length=30, required=True, label='First Name', widget=forms.TextInput(attrs={'placeholder': 'First Name'}))
    last_name = forms.CharField(max_length=30, required=True, label='Last Name', widget=forms.TextInput(attrs={'placeholder': 'Last Name'}))
    username = forms.CharField(max_length=30, required=True, label='Username', widget=forms.TextInput(attrs={'placeholder': 'Username'})) 
    email = forms.EmailField(max_length=254, required=True, label='Email', widget=forms.TextInput(attrs={'placeholder': 'Email'}))


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


class LoginForm(forms.Form):
    username = forms.CharField(required=True, label='Username', widget=forms.TextInput(attrs={'placeholder': 'First Name'}))
    password = forms.CharField(required=True, widget=forms.PasswordInput)
    