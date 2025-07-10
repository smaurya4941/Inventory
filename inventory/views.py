from django.shortcuts import render,redirect,get_object_or_404
from .models import Product,Customer,Purchase,Supplier
from .forms import ProductForm,SupplierForm

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


