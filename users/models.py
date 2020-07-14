from django.db import models
from django.contrib.auth.models import User
import stores.models

# Create your models here.


class Customer(models.Model): 
    """this model handles the store users"""
    user = models.OneToOneField(User, null=True, blank=True, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=200, null=True)
    last_name = models.CharField(max_length=200, null=True)
    username = models.CharField(max_length=200, null=True)
    email = models.EmailField(max_length=200, null=True) 
    phonenumber = models.CharField(max_length=200, null=True)
    device = models.CharField(max_length=200, null=True, blank=True)

    def __str__(self): 
        if self.username:
            name = self.username
        else:
            try:
                name = self.first_name
            except:
                name = self.device
        return str(name)

    @property
    def get_complete_order(self):
        """this property returns the number of completed orders per user"""
        return self.order_set.filter(complete=True).count()

    @property
    def get_amount_spent(self):
        """this property calculates the total spending per customer"""
        #pull all the cart items of products
        orders = self.order_set.all()
        #initialize empty array
        total_price = []
        #loop through all orders
        for order in orders:
            #filter complete orders
            if order.complete:
                #get the order items for complete orders
                order_items = order.orderitem_set.all() 
                #loop through products
                for item in order_items:
                    #add the items price to the array
                    total_price.append(item.product.price)
        #return a sum of the array
        return sum(total_price)
