from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import ensure_csrf_cookie
from django.shortcuts import render
from django.shortcuts import render, redirect
from django.contrib import messages 
from django.contrib.auth.models import User
from datetime import datetime, timedelta
from django.utils.timezone import make_aware

from stores.models import *
from stores.utils import *
from .forms import *

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

    #GENERAL QUERIES
    total_orders = Order.objects.filter(complete=True)

    #quick stats
    #filter the orders within 7 days
    orders_day = total_orders.filter(date_ordered__gte=datetime.now()+timedelta(days=-1)).count()

    #filter the orders within 7 days
    orders_week = total_orders.filter(date_ordered__gte=datetime.now()+timedelta(days=-7)).count()

    #filter the orders within 7 days
    orders_month = total_orders.filter(date_ordered__gte=datetime.now()+timedelta(days=-30)).count()
    
  

    # pending orders
    orders_pending = total_orders.filter(status='Processing').order_by('-date_ordered')
    orders_pending_count = orders_pending.count()

    #registered users
    registered_users = User.objects.all()
    registered_users_count = registered_users.count()
    
    #order statistics
    total_orders_count = total_orders.count()
    total_orders_pending = total_orders.filter(status='Processing').count()
    total_orders_shipped = total_orders.filter(status='Shipped').count()
    total_orders_delivered = total_orders.filter(status='Delivered').count()
     
    #products
    products = Product.objects.all().order_by('-date_added')
    products_count = products.count()
     
    
    
    context = {'cart_quantity': cart_quantity, 'orders_pending':orders_pending, 'orders_pending_count':orders_pending_count,
        'registered_users':registered_users, 'registered_users_count':registered_users_count,
        'total_orders_count':total_orders_count, 'total_orders_pending':total_orders_pending, 
        'total_orders_shipped':total_orders_shipped, 'total_orders_delivered':total_orders_delivered, 'products':products,
        'orders_day':orders_day, 'orders_week':orders_week, 'orders_month':orders_month, 'products_count':products_count,
        }

    return render(request, 'admins/admin_panel.html', context)


def updateOrderStatus(request, order_id):
    """this view handles order status updates"""

    order = Order.objects.get(id=order_id) 
    form = updateOrderStatusForm()

    if request.method == 'POST':
        form = updateOrderStatusForm(request.POST) 

        if form.is_valid():
            status = form.cleaned_data['status']
            order.status = status
            order.save()
            return redirect('/panel') 
            messages.success('Order status was updated')
    else:
        form = updateOrderStatusForm() 

    context = {'form':form,}
    return render(request, 'admins/update_order_status.html', context)


def fullOrderPage(request):
    """this view handles the full order page""" 

     #GENERAL QUERIES
    total_orders = Order.objects.filter(complete=True).order_by('-date_ordered')
    total_orders_count = total_orders.count()

    context = {
        'total_orders':total_orders, 'total_orders_count':total_orders_count, 
        
    
    }
    return render(request, 'admins/full_orders.html', context)



def addProducts(request):
    """this view handles the addition of products""" 

    form = ProductForm()
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)

        if form.is_valid():
            form.save()
            return redirect('panel')
            messages.success(request, 'Your product was saved')
    else:
        form = ProductForm()

    context = {'form':form,}
    return render(request, 'admins/add_products.html', context)