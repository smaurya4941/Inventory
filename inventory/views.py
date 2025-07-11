from django.shortcuts import render,redirect,get_object_or_404
from .models import Product,Customer,Purchase,Supplier
from .forms import ProductForm,SupplierForm,PurchaseForm

# Create your views here.



#********************************PRODUCTS****************************
#view listed product
def view_product(request):
    products=Product.objects.all()
    return render(request,'product/view_product.html',{'products':products})

#add product

def add_product(request):
    if request.method=='POST':
        form=ProductForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('product_list')
    else:
        form=ProductForm()
    return render(request,'product/add_product.html',{'form':form})

#edit product
def edit_product(request,pk):
    product=get_object_or_404(Product,pk=pk)
    # print(product.name)
    form=ProductForm(request.POST or None,instance=product)
    if form.is_valid():
        form.save()
        return redirect('product_list')
    return render(request,'product/add_product.html',{'form':form})


#delete product
def delete_product(request,pk):
    product=get_object_or_404(Product,pk=pk)
    if request.method=='POST':
        product.delete()
        return redirect('product_list')
    return render(request,'product/conf_delete.html',{'product':product})





#*****************************SUPPLIER VIEWS CRUD**********************

#view listed supplier
def view_supplier(request):
    supplier=Supplier.objects.all()
    return render(request,'supplier/view_supplier.html',{'supplier':supplier})

#add supplier
def add_supplier(request):
    if request.method=='POST':
        form=SupplierForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('supplier_list')
    else:
        form=SupplierForm()
    return render(request,'supplier/add_supplier.html',{'form':form})

#edit supplier
def edit_supplier(request,pk):
    supplier=get_object_or_404(Supplier,pk=pk)
    form=SupplierForm(request.POST or None,instance=supplier)
    if form.is_valid():
        form.save()
        return redirect('supplier_list')
    return render(request,'supplier/add_supplier.html',{'form':form})


#delete supplier
def delete_supplier(request,pk):
    supplier=get_object_or_404(Supplier,pk=pk)
    if request.method=='POST':
        supplier.delete()
        return redirect('supplier_list')
    return render(request,'supplier/conf_delete_supplier.html',{'supplier':supplier})




#***********************************PURCHASE  *******************************
#view to purchase product/items from supplier
def purchase_list(request):
    items=Purchase.objects.all()
    return render(request,'purchase/purchase_list.html',{'items':items})

def create_purchase(request):
    if request.method=='POST':
        form=PurchaseForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('purchase_list')
    else:
        form=PurchaseForm()
    return render(request,'purchase/purchase_product.html',{'form':form})

#edit purchase 
def edit_purchase(request,pk):
    item=get_object_or_404(Purchase,pk=pk)
    form=PurchaseForm(request.POST or None,instance=item)
    if form.is_valid():
        form.save()
        return redirect('purchase_list')
    return render(request,'purchase/purchase_product.html',{'form':form})


#delete Purchase
def delete_purchase(request,pk):
    item=get_object_or_404(Purchase,pk=pk)
    if request.method=='POST':
        item.delete()
        return redirect('purchase_list')
    return render(request,'purchase/conf_delete_purchase.html',{'item':item})