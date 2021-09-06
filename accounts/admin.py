from django.contrib import admin
from .models import UserAddress
class UserAddressAdmin(admin.ModelAdmin): 
    class Meta:
        model = UserAddress
admin.site.register(UserAddress, UserAddressAdmin)

# class UserDefaultAddressAdmin(admin.ModelAdmin):
#     class Meta:
#         model = UserDefaultAddress
# admin.site.register(UserDefaultAddress, UserDefaultAddressAdmin)