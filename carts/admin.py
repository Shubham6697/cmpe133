from django.contrib import admin
# To show the models of database on admin url. 
from .models import Cart
from ecommerce.models import Product
from .models import Cart,CartItem

class CartAdmin(admin.ModelAdmin): 
    search_fields = ['__unicode__']
    list_display =['__unicode__', 'id', 'total']
    class Meta:
        model = Cart
admin.site.register(Cart,CartAdmin)


class CartItemAdmin(admin.ModelAdmin):
    list_display =['__str__', 'quantity']
    class Meta:
        model = CartItem
admin.site.register(CartItem, CartItemAdmin)