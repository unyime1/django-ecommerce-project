from django import forms
from django.forms import ModelForm
from stores.models import Product, Order
from django_summernote.widgets import SummernoteWidget, SummernoteInplaceWidget


STATUS = (
    ('Processing', 'Processing'),
    ('Shipped', 'Shipped'),
    ('Delivered', 'Delivered'), 
)

DIGITAL = (
    ('True', 'True'),
    ('False', 'False'), 
)


class updateOrderStatusForm(ModelForm):
    status = forms.ChoiceField(choices=STATUS)

    class Meta:
        model = Order
        fields = ['status']



class ProductForm(ModelForm):
    """this class handles the product addition form"""
    name = forms.CharField(max_length=30, required=True, label='Name',
            widget=forms.TextInput(attrs={'placeholder': ''}))
    price = forms.NumberInput(attrs={'placeholder': 'Price', 'required':True, 'type':'number'})
    description = forms.CharField(widget=SummernoteWidget())

    class Meta:
        model = Product
        fields = '__all__'