from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import ensure_csrf_cookie
from django.shortcuts import render
from django.shortcuts import render, redirect
from django.contrib import messages 
from django.contrib.auth.models import User

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
    orders_pending = Order.objects.filter(status='Processing', complete=True).order_by('-date_ordered')
    orders_pending_count = orders_pending.count()

    #registered users
    registered_users = User.objects.all()
    registered_users_count = registered_users.count()
   

    for user in registered_users:
        user_first_name = user.first_name
        user_last_name = user.last_name
        user_email = user.email
        user_username = user.username
        user_phone = user.customer.phonenumber
       

    context = {'cart_quantity': cart_quantity, 'orders_pending':orders_pending, 'orders_pending_count':orders_pending_count,
        'registered_users':registered_users, 'registered_users_count':registered_users_count, 'user_first_name':user_first_name,
        'user_last_name':user_last_name, 'user_email':user_email, 'user_phone':user_phone, 'user_username':user_username,
       
        }

    return render(request, 'admins/admin_panel.html', context)