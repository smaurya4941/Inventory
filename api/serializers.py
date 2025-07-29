from inventory.models import Product,Supplier,Sale,Purchase,Customer
from django.contrib.auth.models import User
from rest_framework import serializers
from rest_framework.exceptions import ValidationError
#Product models serializer
class ProductSerializer(serializers.ModelSerializer):
    product_name=serializers.SerializerMethodField()
    class Meta:
        model=Product
        fields=['id','product_name','sku','price','quantity','created_at','name']

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
        fields=['id','product_name','customer_name','quantity','sale_price','sale_date','product','customer']

    product_name=serializers.SerializerMethodField()
    customer_name=serializers.SerializerMethodField()

    def get_product_name(self,obj):
        return obj.product.name.name
    
    def get_customer_name(self,obj):
        return obj.customer.name
    

    #logic for creating and updating when new Sale is crated
    def create(self, validated_data):
        product=validated_data['product']
        quantity=validated_data['quantity']

        if(product.quantity<quantity):
            raise ValidationError({'quantity': 'Insufficient product stock available.'})
        
        product.quantity-=quantity
        # validated_data['total_price']=product.price*quantity
        product.save()
        return super().create(validated_data)

#Purchase models serializer
class PurchaseSerializer(serializers.ModelSerializer):
    class Meta:
        model=Purchase
        fields=['id','product_name','supplier_name','quantity','purchase_price','purchase_date','product','supplier']

    product_name=serializers.SerializerMethodField()
    supplier_name=serializers.SerializerMethodField()

    def get_product_name(self,obj):
        return obj.product.name
    
    def get_supplier_name(self,obj):
        return obj.supplier.name
    
      #logic for creating and updating when new Sale is crated
    def create(self, validated_data):
        purchase=Purchase.objects.create(**validated_data)

        if purchase.quantity <= 0:
           raise ValidationError({'quantity': 'Purchase quantity must be greater than 0.'})

    
        purchased_item = purchase.product  # This is your Items model
        purchased_quantity = purchase.quantity
        purchase_price = purchase.purchase_price

        # Check if this Item exists in Product
        existing_product = Product.objects.filter(name=purchased_item).first()

        if existing_product:
            # Update quantity if Product already exists
            existing_product.quantity += purchased_quantity
            existing_product.save()
            
        else:
            # Create new Product if not exists
            Product.objects.create(
                name=purchased_item,
                sku=f"{purchased_item.name[:3].upper()}-{purchased_item.id}",
                description='Auto-created from purchase',
                price=purchase_price,
                quantity=purchased_quantity
            )
        return purchase


#Customer models serializer
class CustomerSerializer(serializers.ModelSerializer):
    class Meta:
        model=Customer
        fields='__all__'

#User models serializer
class UserSerializer(serializers.ModelSerializer): 
    class Meta:
        model=User
        fields=['id','username','email','date_joined']