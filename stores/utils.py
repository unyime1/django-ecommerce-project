from .models import *


def guestUser(request):
    try:
        #get cookie named device
        device = request.COOKIES['device']
    except:
        #get cookie named device
        device = []
    #get or create customer with device id set to device
    customer, created = Customer.objects.get_or_create(device=device)

    return customer