from django.shortcuts import render
from .serializers import ProductSerializer,PurchaseSerializer,CustomerSerializer,SaleSerializer,SupplierSerializers,UserSerializer
from inventory.models import *
from rest_framework import viewsets
from django.contrib.auth.models import User
from rest_framework.authentication import SessionAuthentication
from rest_framework.permissions import IsAuthenticatedOrReadOnly
# Create your views here.

class ProductViewsets(viewsets.ModelViewSet):
    queryset=Product.objects.all()
    serializer_class=ProductSerializer
    authentication_classes=[SessionAuthentication]
    permission_classes=[IsAuthenticatedOrReadOnly]


class PurchaseViewsets(viewsets.ModelViewSet):
    queryset=Purchase.objects.all()
    serializer_class=PurchaseSerializer
    authentication_classes=[SessionAuthentication]
    permission_classes=[IsAuthenticatedOrReadOnly]


class CustomerViewsets(viewsets.ModelViewSet):
    queryset=Customer.objects.all()
    serializer_class=CustomerSerializer
    authentication_classes=[SessionAuthentication]
    permission_classes=[IsAuthenticatedOrReadOnly]

class SupplierViewsets(viewsets.ModelViewSet):
    queryset=Supplier.objects.all()
    serializer_class=SupplierSerializers
    authentication_classes=[SessionAuthentication]
    permission_classes=[IsAuthenticatedOrReadOnly]

class SaleViewsets(viewsets.ModelViewSet):
    queryset=Sale.objects.all()
    serializer_class=SaleSerializer
    authentication_classes=[SessionAuthentication]
    permission_classes=[IsAuthenticatedOrReadOnly]

class UserViewsets(viewsets.ModelViewSet):
    queryset=User.objects.all()
    serializer_class=UserSerializer
    authentication_classes=[SessionAuthentication]
    permission_classes=[IsAuthenticatedOrReadOnly] 