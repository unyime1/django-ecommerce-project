from django import forms


STATUS = (
    ('Processing', 'Processing'),
    ('Shipped', 'Shipped'),
    ('Delivered', 'Delivered'), 
)

class updateOrderStatusForm(forms.Form):
    status = forms.ChoiceField(choices=STATUS)