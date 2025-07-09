from django.db import models

# Create your models here.


#Creating Product Model
class Product(models.Model):
    name=models.CharField(max_length=100)
    sku=models.CharField(max_length=100, unique=True)
    description=models.TextField(blank=True, null=True)
    price=models.DecimalField(max_digits=10,decimal_places=2)
    quantity=models.PositiveIntegerField(default=0)
    created_at=models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f' {self.name} --SKU {self.sku}'


#creating Supplier Model==>seller details
class Supplier(models.Model):
    name=models.CharField(max_length=100)
    contact=models.CharField(max_length=15, blank=True, null=True)
    email=models.EmailField(blank=True, null=True)
    address=models.TextField(blank=True, null=True)
    created_at=models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


#creating a Customer Model
class Customer(models.Model):
    name=models.CharField(max_length=100)
    contact=models.CharField(max_length=15, blank=True, null=True)
    email=models.EmailField(blank=True, null=True)
    address=models.TextField(blank=True, null=True)
    created_at=models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return self.name
    
#creating a Purchase Model==>Products ourchased from supplier
    

class Purchase(models.Model):
    product=models.ForeignKey(Product,on_delete=models.CASCADE)
    supplier=models.ForeignKey(Supplier,on_delete=models.CASCADE)
    quantity=models.PositiveIntegerField()
    purchase_price=models.DecimalField(max_digits=10,decimal_places=2)
    purchase_date=models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return self.product.name
    
    



class Sale(models.Model):
    product=models.ForeignKey(Product,on_delete=models.CASCADE)
    customer=models.ForeignKey(Customer,on_delete=models.CASCADE)
    quantity=models.IntegerField()
    sale_price=models.DecimalField(max_digits=10,decimal_places=2)
    sale_date=models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.customer.name