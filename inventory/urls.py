
from django.contrib import admin
from django.urls import path
from .views import add_product,view_product,edit_product,delete_product
urlpatterns = [
    path('products/create/',add_product,name='add_product'),
    path('products',view_product,name='product_list'),
    path('products/<int:pk>/edit/',edit_product,name='edit_product'),
    path('products/<int:pk>/delete/',delete_product,name='delete_product'),
    
]
