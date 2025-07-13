from django import forms
from .models import Product,Supplier,Purchase,Sale

#******************PRODUCT FORM************
class ProductForm(forms.ModelForm):
    class Meta:
        model=Product
        fields='__all__'



#******************SUPPLIER***********
class SupplierForm(forms.ModelForm):
    class Meta:
        model=Supplier
        fields='__all__'



#*******************PURCHASE PRODUCT FORM*****************
class PurchaseForm(forms.ModelForm):
    class Meta:
        model=Purchase
        fields='__all__'


#*******************Sale PRODUCT FORM*****************
class SaleForm(forms.ModelForm):
    class Meta:
        model=Sale
        fields='__all__'