from django.contrib import admin
from .models import CustomerProfile, Order, Stock, Shop, Product, ShopBucket, OrderProducts

# Register your models here.

admin.site.register(CustomerProfile)
admin.site.register(Product)
admin.site.register(Shop)
admin.site.register(Stock)
admin.site.register(Order)
admin.site.register(ShopBucket)
admin.site.register(OrderProducts)
