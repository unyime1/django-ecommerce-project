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
    name = forms.CharField(max_length=30, required=True, label='Name',
            widget=forms.TextInput(attrs={'placeholder': ''}))
    price = forms.NumberInput(attrs={'placeholder': 'Price', 'required':True, 'type':'number'})
   

    class Meta:
        model = Product
        fields = '__all__'