from django.contrib import admin

from .models import Order
class OrderAdmin(admin.ModelAdmin): 
    list_display = ['__unicode__','order_id','user', 'status', 'finalTotal','shipping_date','shipping_price',]  # custom display of database
    list_editable = ['status','shipping_date']  # edit the price and active status on database directly. You don't need to click on each
    # to filter group in same price , same plug, and active or dec
    list_filter = ['user','status','shipping_date',]
    # To search the related field of order and user
    search_fields = ['user__username']
    readonly_fields = ['user','order_id','ordered_date','shipping_price' ] 
    class Meta:
        model = Order
admin.site.register(Order, OrderAdmin)
# Register your models here.
