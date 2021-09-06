from django.db import models
from carts.models import Cart
from ecommerce.models import User
from datetime import date, timedelta, datetime
from django.conf import settings
import uuid
import decimal



# Python tuples
STATUS_CHOICES = (
    ("Started", "Started"),
    ("Pending", "Pending"), 
    ("Abandoned","Abandoned" ),
    ("Finished", "Finished"), 
)

oneDay_price = 9.99
threeDays_price= 4.99
sevenDays_price = 0.00
# SHIPPING fee
SHIPPING_PRICE = (
    (oneDay_price,oneDay_price),
    (threeDays_price,threeDays_price), 
    (sevenDays_price,sevenDays_price),)

class Order(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete= models.CASCADE, )# total price with tax
    subTotal = models.DecimalField(max_digits=1000, decimal_places=2, default=0.00) #  total price without tax
    taxTotal = models.DecimalField(max_digits=1000, decimal_places=2, default=0.09) #  tax price
    finalTotal = models.DecimalField(max_digits=1000, decimal_places=2, default=0.00) #  final total 
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    order_id =  models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    status = models.CharField(max_length=120, choices=STATUS_CHOICES, default="Started")
    start_date  = models.DateTimeField(auto_now=False, auto_now_add=True) 
    ordered_date = models.DateTimeField(auto_now=True, auto_now_add=False) #last day of updating the cart that means checkout date
    shipping_date = models.DateField(null = True, blank=True)
    shipping_price = models.DecimalField(max_digits=100, decimal_places=2, default= 0.00)
    # Return the string on database
    def __unicode__(self):
        return self.user.username

    #  To calculate the shipping fee  follow to 1, 3, 7 days
    # https://www.pythonprogramming.in/how-to-calculate-the-time-difference-between-two-datetime-objects.html
    # https://stackoverflow.com/questions/37093454/typeerror-must-be-string-not-datetime-datetime-when-using-strptime
    def shipping_fee(self): 
        oneDay = 2
        threeDays = 5
        sevenDays = 7

        # Format the datetime of ordered date
        ordered_date = datetime.strptime(str(self.ordered_date),"%Y-%m-%d %H:%M:%S.%f+00:00")
        # Calculate the total day
        total_date  = (self.shipping_date - ordered_date)
        day = int(total_date.days )
        if int(day) <=  oneDay:
            shipping_price = oneDay_price
        elif int(day) > oneDay and   int(day) < sevenDays:
            shipping_price = threeDays_price
        elif int(day) >= sevenDays:
            shipping_price = sevenDays_price
        print(day)
        self.shipping_price = decimal.Decimal(shipping_price)
        self.save()

        
        


        