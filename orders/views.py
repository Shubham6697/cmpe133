from django.shortcuts import render, HttpResponseRedirect
from .models import *
from ecommerce.models import Product
from django.contrib.auth.decorators import login_required
from ecommerce.views import *
from carts.views import *
from django.urls import reverse
from django.contrib.sessions.models import Session
import time
import math
from accounts.models import *
from .models import * 
from accounts.views import *
import decimal
from datetime import date, timedelta

# to create a new order
@login_required
def checkout(request):
    # To get the cart currently 
    try: 
            cart = Cart.objects.get(user = request.user, ordered=False)
    except: 
            cart = None
            return HttpResponseRedirect(reverse('cart'))
#--------------------------------------------------------------------
    #To get the order, if not create a new one
    try: 
        new_order  = Order.objects.get(user = request.user, cart=cart )
    except Order.DoesNotExist: 
        new_order = Order.objects.create(user = request.user,cart=cart)
# ----------------------------------------------------------------------
    # To calculate all total of cart in checkout
    total = cart.total 
    new_order.subTotal = total
    new_order.save()

    finalTotal = (decimal.Decimal(new_order.subTotal) + decimal.Decimal(new_order.subTotal) * decimal.Decimal(new_order.taxTotal)) + decimal.Decimal(new_order.shipping_price) 
    new_order.finalTotal = round(finalTotal,2)
    new_order.save()
#------------------------------------------------------------------------
    today = date.today()
    one_day = today + timedelta(days=2)
    three_days = today+timedelta(days=5)
    seven_days =  today + timedelta(days=9)

    order = Order.objects.get(user = request.user, cart=cart )

# -----------------------------------------------------------------
    # To change the address or add the new address
    try: 
        addressDefault = UserAddress.objects.get(user = request.user)
        context={'address1' : True, 'address':addressDefault, "order": order,'cart':cart , 'one_day':one_day,'three_days':three_days, 'seven_days':seven_days}
    except:
        addressDefault= None
        message = " No Address In Your Account"
        context = { "address1": False, "message": message, "order": order,'cart':cart}
           
    if request.method == 'POST':
        address = request.POST['address']
        city = request.POST['city']
        state = request.POST['state']
        zipcode = request.POST['zipcode']
        phone_number = request.POST['phone_number']

        if addressDefault != None: 
                addressDefault.address = address
                addressDefault.city = city
                addressDefault.state = state
                addressDefault.zipcode = zipcode
                addressDefault.phone_number = phone_number
                addressDefault.save()
                messages.success(request, 'Saved successfully')
                return HttpResponseRedirect(reverse('checkout'))
        elif addressDefault == None:
                new_address = UserAddress.objects.create(user=request.user, address=address, city = city, state=state, zipcode=zipcode, phone_number=phone_number)
                new_address.save()
                return HttpResponseRedirect(reverse('checkout'))

    template = 'checkout/checkout.html'
    return render(request,template,context)

# ----------------------------------------------------------------------------------------------------------------
# To solve the time shipping and fee shipping
@login_required
def time_shipping(request):
    try: 
            cart = Cart.objects.get(user = request.user, ordered=False)
    except: 
            cart = None
            return HttpResponseRedirect(reverse('cart'))

    # declare the date today. next 3 days,  7 days
    today = date.today()
    one_day = today + timedelta(days=1)
    three_days = today+timedelta(days=4)
    seven_days = today + timedelta(days=7)


    try: 
        new_order  = Order.objects.get(user = request.user, cart=cart )
    except Order.DoesNotExist: 
        new_order = Order.objects.create(user = request.user,cart=cart)
        new_order  = Order.objects.get(user = request.user, cart=cart )


    # To input the shipping time
    if request.method == 'POST':
        shipping_date = request.POST['shipping_date']

        # Convert the true format date for the database
        shipping_date = datetime.strptime(shipping_date,"%B %d, %Y")
        new_order.shipping_date = shipping_date
        new_order.save()

        # To calculate the shipping fee
        Order.shipping_fee(new_order)

    return redirect(checkout) 

#--------------------------------------------------------------------------------------------------
#  To save the order on the database
def orders(request): 
    # Finshed order
    cart = Cart.objects.get(user = request.user, ordered=False)
    new_order  = Order.objects.get(user = request.user, cart=cart )
    new_order.status = "Pending"
    new_order.save()
    cart.ordered = True
    cart.save()

    #  The badge on cart
    request.session['key'] = 0

    return HttpResponseRedirect(reverse('homeMain'))
