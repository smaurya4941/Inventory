from django.shortcuts import render,redirect,get_object_or_404
from .models import Product,Customer,Purchase,Supplier,Sale
from .forms import ProductForm,SupplierForm,PurchaseForm,SaleForm

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
#list all purchased items
def purchase_list(request):
    items=Purchase.objects.all()
    return render(request,'purchase/purchase_list.html',{'items':items})
#view to purchase product/items from supplier
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


#*******************SALES VIEWS*************************

#list of all sales
def sales_list(request):
    product=Sale.objects.all()
    return render(request,'sales/sales_list.html',{'product':product})

#create_sales

def create_sale(request):
    if request.method=='POST':
        form=SaleForm(request.POST)
        if form.is_valid():
            sale=form.save(commit=False)
            product=sale.product
            if product.quantity>=sale.quantity:
                product.quantity-=sale.quantity #decreasing the sold items from remaining items
                product.save()
                sale.save()
                return redirect('sales_list')
            else:
                form.add_error('quantity',"Not enough items available")
    else:
        form=SaleForm()
    return render(request,'sales/sales_product.html',{'form':form})

#edit sales
def edit_sales(request,pk):
    sales=get_object_or_404(Sale,pk=pk)
    form=SaleForm(request.POST or None,instance=sales)
    if form.is_valid():
        form.save()
        return redirect('sales_list')
    return render(request,'sales/sales_product.html',{'form':form})


#delete the sales
def delete_sales(request,pk):
    sale=get_object_or_404(Sale,pk=pk)
    if request.method=='POST':
        product=sale.product
        product.quantity+=sale.quantity
        product.save()
        sale.delete()
        return redirect('sales_list')
    return render(request,'sales/conf_delete_sale.html',{'sale':sale})
    

#*****************************DASHBOARD ********************************

def dashboard(request):
    return render(request,'dashboard/dashboard.html')


def index(request):
    return render(request,'dashboard/index.html')