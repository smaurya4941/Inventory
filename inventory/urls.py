
from django.contrib import admin
from django.urls import path
from .views import *
urlpatterns = [

    #********PRODUCTS*****************
    path('products/create/',add_product,name='add_product'),
    path('products/',view_product,name='product_list'),
    path('products/<int:pk>/edit/',edit_product,name='edit_product'),
    path('products/<int:pk>/delete/',delete_product,name='delete_product'),

    #***********SUPPLIER*******************
    path('suppliers/create/',add_supplier,name='add_supplier'),
    path('suppliers/',view_supplier,name='supplier_list'),
    path('suppliers/<int:pk>/edit/',edit_supplier,name='edit_supplier'),
    path('suppliers/<int:pk>/delete/',delete_supplier,name='delete_supplier'),

    #**************PURCHASE*****************
    path('purchase/',purchase_list,name='purchase_list'),
    path('purchase/create',create_purchase,name='create_purchase'),
    path('purchase/<int:pk>/edit',edit_purchase,name='edit_purchase'),
    path('purchase/<int:pk>/delete',delete_purchase,name='delete_purchase'),

    #******************SALES********************
    path('sales/',sales_list,name='sales_list'),
    path('sales/sales_product',create_sale,name='create_sale'),
    path('sales/<int:pk>/edit_sales',edit_sales,name='edit_sales'),
    path('sales/<int:pk>/delete_sales',delete_sales,name='delete_sales'),
    

    #************DASHBOARD*************
    path('',dashboard,name='dashboard'),      
]
