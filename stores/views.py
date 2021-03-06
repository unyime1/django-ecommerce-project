from django.shortcuts import render, redirect
from django.http import JsonResponse
import json
import datetime
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import ensure_csrf_cookie
from django.contrib import messages 

# Create your views here.
from .models import *
from .utils import *
from .decorators import *
 
@ensure_csrf_cookie
def home(request):
    """this function handles the home view"""

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
    return render(request, 'stores/home.html', context)


@ensure_csrf_cookie
def store(request):
    """this function handles the store view"""

    products = Product.objects.all().order_by('-date_added')

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
    
    context = {'products': products, 'cart_quantity':cart_quantity}
    return render(request, 'stores/store.html', context)


@ensure_csrf_cookie
def checkout(request):
    """this function handles the checkout view"""

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

    context = {'items':items, 'order':order,'cart_quantity': cart_quantity}
    return render(request, 'stores/checkout.html', context)


@ensure_csrf_cookie
def contact(request):
    """this function handles the contact view"""

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
    return render(request, 'stores/contact.html', context)


@ensure_csrf_cookie
def cart(request):
    """this function handles the cart view"""

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
 
    context = {'items':items, 'order':order, 'cart_quantity': cart_quantity}
    return render(request, 'stores/cart.html', context)


def updateItem(request):
    """this function handles the update cart functionality"""

    #get the data from the api response body
    data = json.loads(request.body)
    productId = data['productId']
    action = data['action']

    
    
    try:
        #query customer and product data
        customer = request.user.customer
    except:
        #get cookie named device
        device = request.COOKIES['device']
        #get or create customer with device id set to device
        customer, created = Customer.objects.get_or_create(device=device)

    
    product = Product.objects.get(id=productId)
    #query or create order
    order, created = Order.objects.get_or_create(customer=customer, complete=False)
    #query or create order items associated with the other
    orderItem, created = OrderItem.objects.get_or_create(order=order, product=product)

    # update product quantity depending on the action taken by user
    if action == 'add':
        orderItem.quantity += 1

    elif action == 'remove':
        orderItem.quantity -= 1
    
    orderItem.save()

    if orderItem.quantity <= 0:
        orderItem.delete()

    return JsonResponse('Item was added', safe=False)



def processOrder(request):
    """this function handles order processing"""

    #load json data from the request body
    data = json.loads(request.body)

    #generate a transaction id
    transaction_id = datetime.datetime.now().timestamp()
    
    #get the customer data if the customer is logged in
    if request.user.is_authenticated:
        customer = request.user.customer
        customer.phonenumber = data['form']['phonenumber']
        customer.save() 
        
    else:
        #get cookie named device
        device = request.COOKIES['device']
        #get or create customer with device id set to device
        customer, created = Customer.objects.get_or_create(device=device)
        #store name and email of the anonymous user from the checkout form
        customer.first_name = data['form']['first_name']
        customer.last_name = data['form']['last_name']
        customer.email = data['form']['email']
        customer.phonenumber = data['form']['phonenumber']
        customer.save() 
      
        

    #query or create the order
    order, created = Order.objects.get_or_create(customer=customer, complete=False)
    #get total amount from the json data
    total = float(data['form']['total'])
    order.transaction_id = transaction_id

    #since the payment total is processed at the front end before sending to backend
    #we need to conform that both the frontend and backend totals are the same before processing order
    if total == order.get_cart_total:
        order.complete = True
        order.save()
    else:
        order.delete()

    if order.shipping == True:
        ShippingAddress.objects.create(
            customer=customer,
            order=order,
            #access shipping information from the json data sent from checkout.js
            address=data['shipping']['address'],
            city=data['shipping']['city'],
            state=data['shipping']['state'],
            zipcode=data['shipping']['zipcode'],
            country=data['shipping']['country'],
        )

    return JsonResponse('Payment complete', safe=False)


@ensure_csrf_cookie
@admin_only
@login_required(login_url='login')
def orderDetailsPage(request, order_id):
    """This function renders the view that gives the detailed overview of individual orders"""

    if request.user.is_authenticated:
        customer = request.user.customer

    else:
        #get the guest user logic from utils.py module
        customer = guestUser(request) 

    #get customer's uncompleted orders(open cart). If none, create the order.
    order_c, created = Order.objects.get_or_create(customer=customer, complete=False)

    #get cart items from order model property
    cart_quantity = order_c.get_cart_quantity 

    #database queries
    order = Order.objects.get(id=order_id)
    shipping_information = order.shippingaddress_set.get(order=order.id)
    product_information = order.orderitem_set.all()

    context = {'order':order, 'shipping_information':shipping_information,
        'product_information':product_information, 'cart_quantity':cart_quantity,}
    return render(request, 'stores/order_page.html', context)


@ensure_csrf_cookie
def productPage(request, product_id):
    """this function handles the product page"""

    product = Product.objects.get(id=product_id)

    if request.user.is_authenticated:
        customer = request.user.customer

    else:
        #get the guest user logic from utils.py module
        customer = guestUser(request)


    #get customer's uncompleted orders(open cart). If none, create the order.
    order, created = Order.objects.get_or_create(customer=customer, complete=False)


    #get cart items from order model property
    cart_quantity = order.get_cart_quantity 
    
    context = {'product': product, 'cart_quantity':cart_quantity}
    return render(request, 'stores/product_page.html', context)
