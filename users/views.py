from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.models import Group #database groups
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required

# Create your views here.
from stores.models import *
from stores.utils import *
from .forms import *
from stores.decorators import *

 
@unauthenticated_users
def userRegistration(request):
    """this function handles the register view"""

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

    #user registration logic
    form = RegistrationForm()
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
            #checks if form submission is valid
        if form.is_valid():
            user = form.save()

            #add user to the customer group
            group = Group.objects.get(name='customer')
            user.groups.add(group)

            
            #add registered user to Customer model
            Customer.objects.create(
                user = user,
                first_name = user.first_name,
                last_name = user.last_name,
                username = user.username,
                email = user.email,
            )

            #query username for flash message
            first_name = form.cleaned_data.get('first_name')
            last_name = form.cleaned_data.get('last_name')

            messages.success(request, 'Account was created for ' + first_name + ' ' + last_name + '.')
            return redirect('login')
    else:
        form = RegistrationForm()

    context = {'cart_quantity': cart_quantity, 'form': form}
    return render(request, 'users/register.html', context)


@unauthenticated_users
def userLogin(request):
    """this function handles the login view"""

    #user login logic

    #pull login data from form
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        #authenticate the user
        user = authenticate(request, username=username, password=password)

        #login user
        if user is not None:
            login(request, user)
            return redirect('profile')
        else:
            messages.info(request, 'username or password is incorrect!')
            return redirect('login')


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

    context = {'cart_quantity': cart_quantity}
    return render(request, 'users/login.html', context)


def userLogout(request):
    """this function handles the logout functionality"""

    logout(request)
    return redirect('login')


@login_required(login_url='login')
def userProfile(request):
    """this function handles the profile view"""
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

    #user profile logic

    #database queries
    customer = request.user.customer
    orders = request.user.customer.order_set.all().filter(complete='True')
    total_orders = orders.count()
    delivered = orders.filter(status='Delivered').count()
    processing = orders.filter(status='Processing').count()
    shipped = orders.filter(status='Shipped').count()

    context = {'cart_quantity': cart_quantity, 'orders': orders,
                'total_orders': total_orders, 'delivered': delivered,
                'processing': processing, 'shipped': shipped, 'customer':customer}
    return render(request, 'users/profile.html', context)

