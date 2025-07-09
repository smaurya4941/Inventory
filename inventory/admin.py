from django.contrib import admin
from .models import Product,Supplier,Purchase,Customer,Sale
# Register your models here.

admin.site.register(Product)
admin.site.register(Supplier)
admin.site.register(Purchase)
admin.site.register(Customer)
admin.site.register(Sale)