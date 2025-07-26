from django.shortcuts import render
from .serializers import ProductSerializer,PurchaseSerializer,CustomerSerializer,SaleSerializer,SupplierSerializers,UserSerializer
from inventory.models import *
from rest_framework import viewsets
from django.contrib.auth.models import User
# Create your views here.

class ProductViewsets(viewsets.ModelViewSet):
    queryset=Product.objects.all()
    serializer_class=ProductSerializer


class PurchaseViewsets(viewsets.ModelViewSet):
    queryset=Purchase.objects.all()
    serializer_class=PurchaseSerializer


class CustomerViewsets(viewsets.ModelViewSet):
    queryset=Customer.objects.all()
    serializer_class=CustomerSerializer

class SupplierViewsets(viewsets.ModelViewSet):
    queryset=Supplier.objects.all()
    serializer_class=SupplierSerializers

class SaleViewsets(viewsets.ModelViewSet):
    queryset=Sale.objects.all()
    serializer_class=SaleSerializer

class UserViewsets(viewsets.ModelViewSet):
    queryset=User.objects.all()
    serializer_class=UserSerializer