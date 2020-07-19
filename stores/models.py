from django.db import models

# import the Customer model from users app
from users.models import Customer
 
class Product(models.Model):
    """this model handles the products in store"""
    name = models.CharField(max_length=200, null=True)
    price = models.FloatField()
    digital = models.BooleanField(default=False, null=True, blank=True)
    date_added = models.DateTimeField(auto_now_add=True, null=True)
    image = models.ImageField(default='placeholder.png', null=True, blank=True, upload_to='images/')

    def __str__(self):
        return self.name  

    @property
    def imageURL(self):
        """this function solves the error associated with empty image fields"""
        try:
            url = self.image.url
        except:
            url = ''
        return url

    @property
    def get_product_count(self):
        """this property counts the total amount of purchases per product"""
        #pull all the cart items of products
        order_item = self.orderitem_set.all()
        #initialize empty array
        total = []
        #loop through products
        for orders in order_item:
            #check if the order was completed
            if orders.order.complete:
                #add the items quantity in completed orders to array
                total.append(orders.quantity)
        #return a sum of the array
        return sum(total)



class Order(models.Model):
    """this model handles the customer orders"""

    STATUS = (
        ('Processing', 'Processing'),
        ('Shipped', 'Shipped'),
        ('Delivered', 'Delivered'), 
    )

    customer = models.ForeignKey(Customer, null=True, blank=True, on_delete=models.SET_NULL)
    date_ordered = models.DateTimeField(auto_now_add=True)
    complete = models.BooleanField(default=False, null=True, blank=False)
    status = models.CharField(max_length=200, null=True, blank=True, choices=STATUS, default='Processing')
    transaction_id = models.CharField(max_length=200, null=True)

    def __str__(self):
        return str(self.customer.name) 

    @property
    def shipping(self):
        """this function determines of an item is eligible for shipping or not"""
        #initialize shipping to false
        shipping = False
        #query the items on cart and check if any has digital products set to false
        #enable shipping if they do
        orderitems = self.orderitem_set.all()
        for orderitem in orderitems:
            if orderitem.product.digital == False:
                shipping = True
        return shipping


    @property
    def get_cart_total(self):
        """this function gets the total cost of all the items in the cart"""
        #query the OrderItem table for items on this particular order
        orderitems = self.orderitem_set.all()
        #loop through the orderitems list and sum their total costs
        total = sum([item.get_total_cost for item in orderitems])
        #return the total cost
        return total

    @property
    def get_cart_quantity(self):
        """this function gets the quantity of items in the cart"""
        #query the OrderItem table for items on this particular order
        orderitems = self.orderitem_set.all()
        #loop through the orderitems list and get their quantity
        total = sum([item.quantity for item in orderitems])
        #return the total cost
        return total

    


class OrderItem(models.Model):
    """this model handles the datails of a particular item to be purchased"""
    product = models.ForeignKey(Product, null=True, blank=True, on_delete=models.SET_NULL)
    order = models.ForeignKey(Order, null=True, blank=True, on_delete=models.SET_NULL)
    quantity = models.IntegerField(default=0, null=True, blank=True)
    date_added = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.product.name
 
    @property
    def get_total_cost(self):
        """this function computes the total cost of a particular item to be purchased"""
        total = self.product.price * self.quantity
        return total

    
        

class ShippingAddress(models.Model):
    customer = models.ForeignKey(Customer, null=True, blank=True, on_delete=models.SET_NULL)
    order = models.ForeignKey(Order, null=True, blank=True, on_delete=models.SET_NULL)
    address = models.CharField(max_length=200, null=True)
    city = models.CharField(max_length=200, null=True)
    state = models.CharField(max_length=200, null=True)
    zipcode = models.CharField(max_length=200, null=True)
    country = models.CharField(max_length=200, null=True)
    date_added = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.address
