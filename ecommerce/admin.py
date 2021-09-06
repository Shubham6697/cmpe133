from django.contrib import admin
from .models import Product, ProductImage, Contact


# This page to upload the database on admin site

# Custom view of database Product
class ProductAdmin(admin.ModelAdmin):
    date_hierarchy = 'timestamp'  # show the time filter on database
    # create search function on database
    search_fields = ['title', 'description', 'salePrice', 'category']
    list_display = ['__str__', 'title', 'price','salePrice','category', 
                    'active', 'updated',]  # custom display of database
    # list_display = [ 'title', 'price', 'active', 'updated']
    list_editable = ['salePrice',
                     'active', 'category']  # edit the price and active status on database directly. You don't need to click on each
    # to filter group in same price , same plug, and active or dec
    list_filter = ['price', 'slug', 'active', 'category']

    readonly_fields = ['updated', 'timestamp']  # show only, cant fix variables
    # auto update slug ==  title when adding new product
    prepopulated_fields = {"slug": ("title", "salePrice",)}

    class Meta:
        model = Product


class ImageProductAdmin(admin.ModelAdmin):
    list_display = ['__str__', 'image']
    list_filter = ['product']

    class Meta:
        model = ProductImage

class ContactAdmin(admin.ModelAdmin): 
    list_display = ['__str__','email','solved_status', 'timestamp']
    readonly_fields = ['email','firstName', 'lastName', 'timestamp','message'] 
    list_editable = ['solved_status'] 
    search_fields = ['solved_status', 'email', 'user']
    list_filter = ['solved_status']

     # show only, cant fix variables
    class Meta:
        model = Product

# Add the database Product to admin
admin.site.register(Product, ProductAdmin)
admin.site.register(ProductImage, ImageProductAdmin)
admin.site.register(Contact, ContactAdmin)


    


