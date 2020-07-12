from django.db import models
from django.contrib.auth.models import User

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

 