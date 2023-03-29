from django.contrib import admin
from .models import *
# Register your models here.

class CategoryAdmin(admin.ModelAdmin): 
    list_display = ['name']

class ProductAdmin(admin.ModelAdmin):
    list_display = ['name','price','image']

admin.site.register(Product,ProductAdmin)
admin.site.register(Category,CategoryAdmin)

class CustomerAdmin(admin.ModelAdmin):
    list_display = ['firstname','lastname','email','password']

class OrderAdmin(admin.ModelAdmin):
    list_display = ['country','state','street','building','houseno','postalno','zip']

admin.site.register(Customer,CustomerAdmin)
admin.site.register(Cart)
admin.site.register(CartItem)
admin.site.register(OrderDetails,OrderAdmin)






