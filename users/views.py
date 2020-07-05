from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.models import Group #database groups
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import ensure_csrf_cookie

#for confirmation emails
from django.contrib.sites.shortcuts import get_current_site
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_text
from django.template.loader import render_to_string
from .token import account_activation_token
from django.core.mail import EmailMessage

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
            user = form.save(commit=False)
            user.is_active = False
            user.save()

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

            messages.success(request, 'Account was created for ' + first_name + ' ' + last_name + '.' + ' Visit you mail to activate your account')

            #send activation mail
            current_site = get_current_site(request)
            email_subject = 'Activate Your Account'
            message = render_to_string('users/activate_account.html', {
                'user': user,
                'domain': current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': account_activation_token.make_token(user),
            })
            to_email = form.cleaned_data.get('email')
            email = EmailMessage(email_subject, message, to=[to_email])
            email.send()

            return redirect('login')
    else:
        form = RegistrationForm()

    context = {'cart_quantity': cart_quantity, 'form': form}
    return render(request, 'users/register.html', context)



def activate_account(request, uidb64, token):
    """function for account activation"""
    try:
        uid = force_bytes(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        login(request, user)
        return HttpResponse('Your account has been activated successfully')
    else:
        return HttpResponse('Activation link is invalid!')



@unauthenticated_users
def userLogin(request):
    """this function handles the login view"""

    #user login logic
    form = LoginForm()
    #pull login data from form
    if request.method == "POST":
        form = LoginForm(request.POST)

        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            
            #authenticate the user
            user = authenticate(request, username=username, password=password)

            #login user
            if user is not None:
                login(request, user)
                return redirect('profile')
            else:
                messages.info(request, 'username or password is incorrect!')
                return redirect('login')
    else:
        form = LoginForm()


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

    context = {'cart_quantity': cart_quantity, 'form':form}
    return render(request, 'users/login.html', context)


def userLogout(request):
    """this function handles the logout functionality"""

    logout(request)
    return redirect('login')


@ensure_csrf_cookie
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

