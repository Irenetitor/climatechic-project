from django.contrib import admin

from store.models import Order, OrderItem, Product, ShippingAddress

# Register your models here.

admin.site.register(Product)
admin.site.register(Order)
admin.site.register(OrderItem)
admin.site.register(ShippingAddress)