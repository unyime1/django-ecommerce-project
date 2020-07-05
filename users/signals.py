""" This module handles signal related functions"""

from django.db.models.signals import post_save
from django.db.models.signals import pre_save
from django.contrib.auth.models import User
from .models import Customer
from django.contrib.auth.models import Group




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