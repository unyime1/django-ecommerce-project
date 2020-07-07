""" This module handles signal related functions"""

from django.db.models.signals import post_save
from django.contrib.auth.models import User
from .models import Customer
from django.contrib.auth.models import Group
from django.core import mail
from django.template.loader import render_to_string
#from django.contrib.sites.models import Site

from stores.models import Order
from stores.models import ShippingAddress




def customer_profile(sender, instance, created, **kwargs):
    """this function handles the creation of users"""
    
    if created: #check if this is the first instance
        #add registered user to customer group
        group = Group.objects.get(name='customer') #query customer group in admin
        instance.groups.add(group)  #add instance of user to the queried group

        #to avoid errors when a registered user visits the user page, we have to add the user to the 'user' table of the Customer model
        Customer.objects.create(    #
            user=instance, 
            first_name = instance.first_name,
            last_name = instance.last_name,
            username = instance.username,
            email = instance.email,
        )

post_save.connect(customer_profile, sender=User) 



def order_confirmation_email(sender, instance, **kwargs):
    """this function sends order confirmation emails"""
   
    customer = instance.customer
    order = instance.order
    #current_site = Site.objects.get_current()

    customer_message = render_to_string('users/customer_order_confirmation.html', {
            'customer': customer,
            'order':order,
            #'domain': current_site.domain,
        })

    admin_message = render_to_string('users/admin_order_email.html', {
            'customer': customer,
            'order':order,
            #'domain': current_site.domain,
        })

    connection = mail.get_connection()

    # Manually open the connection
    connection.open()

    # Construct an email message that uses the connection
    email1 = mail.EmailMessage(
        'Order Confirmation',
        customer_message,
        'from@example.com',
        [customer.email],
        connection=connection,
    )

    # Construct two more messages
    email2 = mail.EmailMessage(
        'Order Notification',
        admin_message,
        'from@example.com',
        ['lordunyime@yahoo.com'],
    )
    

    # Send the two emails in a single call -
    connection.send_messages([email1, email2])
    # The connection was already open so send_messages() doesn't close it.
    # We need to manually close the connection.
    connection.close()

post_save.connect(order_confirmation_email, sender=ShippingAddress) 