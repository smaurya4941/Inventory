from inventory.models import Product,Supplier,Sale,Purchase,Customer
from django.contrib.auth.models import User
from rest_framework import serializers
#Product models serializer
class ProductSerializer(serializers.ModelSerializer):
    product_name=serializers.SerializerMethodField()
    class Meta:
        model=Product
        fields=['id','product_name','sku','price','quantity','created_at']

    def get_product_name(self,obj):
        return obj.name.name

#Supplier models serializer
class SupplierSerializers(serializers.ModelSerializer):
    class Meta:
        model=Supplier
        fields=['id','name','email','created_at']

#Sale models serializer
class SaleSerializer(serializers.ModelSerializer):
    class Meta:
        model=Sale
        fields=['id','product_name','customer_name','quantity','sale_price','sale_date']

    product_name=serializers.SerializerMethodField()
    customer_name=serializers.SerializerMethodField()

    def get_product_name(self,obj):
        return obj.product.name.name
    
    def get_customer_name(self,obj):
        return obj.customer.name
    

#Purchase models serializer
class PurchaseSerializer(serializers.ModelSerializer):
    class Meta:
        model=Purchase
        fields=['id','product_name','supplier_name','quantity','purchase_price','purchase_date']

    product_name=serializers.SerializerMethodField()
    supplier_name=serializers.SerializerMethodField()

    def get_product_name(self,obj):
        return obj.product.name
    
    def get_supplier_name(self,obj):
        return obj.supplier.name



#Customer models serializer
class CustomerSerializer(serializers.ModelSerializer):
    class Meta:
        model=Customer
        fields='__all__'

#User models serializer
class UserSerializer(serializers.ModelSerializer):
    # date_joined=serializers.DateTimeField(format="%d-%m-%Y") 
    class Meta:
        model=User
        fields=['id','username','email','date_joined']