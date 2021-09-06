from django.db import models
from ecommerce.models import Product, User
from datetime import datetime
from django.conf import settings

class CartItem(models.Model): 
    cart = models.ForeignKey('Cart', null=True, blank=True, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)
    productTotal = models.DecimalField(max_digits=1000, decimal_places=2, default=1.00)
    start_date  = models.DateTimeField(auto_now=False, auto_now_add=True) 
    ordered_date = models.DateTimeField(auto_now=True, auto_now_add=False) 
    imageName = models.CharField( max_length=10000, null=True, blank= True)
    
    # def total_price_of_product(self):
    #     totalProduct = product.salePrice * self.quantity
    #     return totalProduct
        
    def __unicode__(self):
        try: 
            return str(self.cart.id)
        except:
            return self.product.title

    def totalItem(self):
        totalAll = float(self.product.salePrice) * float(self.quantity)
        self.productTotal = totalAll
        self.save()
        
class Cart(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete= models.CASCADE, )# total price with tax
    total = models.DecimalField(max_digits=100, decimal_places=2, default=0.00) #  total price without tax
    totalCount = models.IntegerField(default=0)
    start_date  = models.DateTimeField(auto_now=False, auto_now_add=True) 
    ordered_date = models.DateTimeField(auto_now=True, auto_now_add=False) #last day of updating the cart that means checkout date
    ordered = models.BooleanField(default=False)# status of a cart have been checkout or not

    def __unicode__(self):
        return self.id
    
    def cartTotal(self):
        total = 0.00
        for item in self.cartitem_set.all():
                total += float(item.productTotal)
        self.total = total
        self.save()








