from django import forms
from django.forms import ModelForm
from stores.models import Product


STATUS = (
    ('Processing', 'Processing'),
    ('Shipped', 'Shipped'),
    ('Delivered', 'Delivered'), 
)

DIGITAL = (
    ('True', 'True'),
    ('False', 'False'),
)


class updateOrderStatusForm(forms.Form):
    status = forms.ChoiceField(choices=STATUS)



class ProductForm(ModelForm):
    """this class handles the product addition form"""
    name = forms.CharField(max_length=30, required=True, label='Product Name',
            widget=forms.TextInput(attrs={'placeholder': 'Product Name'}))
    price = forms.NumberInput()
    image = forms.ImageField(required=True)
    digital = forms.BooleanField(required=True)

    class Meta:
        model = Product
        fields = '__all__'