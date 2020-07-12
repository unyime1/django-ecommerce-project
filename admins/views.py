from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import ensure_csrf_cookie
from django.shortcuts import render
from django.shortcuts import render, redirect
from django.contrib import messages 

from stores.models import *
from stores.utils import *

# Create your views here.


@ensure_csrf_cookie
@login_required(login_url='login')
def adminPanel(request):
    """this view handles the admin panel"""

    if request.user.is_authenticated:
        customer = request.user.customer

    else:
        #get the guest user logic from utils.py module
        customer = guestUser(request)

    #get customer's uncompleted orders(open cart). If none, create the order.
    order, created = Order.objects.get_or_create(customer=customer, complete=False)

    #get all the items associated with that particular order
    #take note of the reverse search
    items = order.orderitem_set.all() 

    #get cart items from order model property
    cart_quantity = order.get_cart_quantity

    # queries for pending order table
    orders = Order.objects.filter(status='Processing').order_by('-date_ordered')

    context = {'cart_quantity': cart_quantity, 'orders':orders}

    return render(request, 'admins/admin_panel.html', context)