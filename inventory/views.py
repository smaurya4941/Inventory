from django.shortcuts import render,redirect,get_object_or_404
from .models import Product,Customer,Purchase,Supplier,Sale
from .forms import ProductForm,SupplierForm,PurchaseForm,SaleForm
from django.db.models import F, Sum, FloatField
# Create your views here.



#********************************PRODUCTS****************************
#view listed product
def view_product(request):
    query = request.GET.get('q')
    if query:
        products = Product.objects.filter(name__icontains=query) | Product.objects.filter(sku__icontains=query)
    else:
        products = Product.objects.all()

    for product in products:
        product.total_cost=product.quantity * product.price
    return render(request,'product/view_product.html',{'products':products,'query':query})

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
    query=request.GET.get('q')
    if query:
        supplier=Supplier.objects.filter(name__icontains=query) | Supplier.objects.filter(address__icontains=query)
    else:
        supplier=Supplier.objects.all()
    return render(request,'supplier/view_supplier.html',{'supplier':supplier,'query':query})

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
    query=request.GET.get('q')
    products = Product.objects.all()
    if query:
        items=Purchase.objects.filter(product__name__icontains=query) | Purchase.objects.filter(supplier__name__icontains=query)
    else:
        items=Purchase.objects.all()
    return render(request,'purchase/purchase_list.html',{'items':items,'query':query,'products':products})
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
    query=request.GET.get('q')
    if query:
        product=Sale.objects.filter(product__name__icontains=query) | Sale.objects.filter(customer__name__icontains=query)
    else:
        product=Sale.objects.all()
    return render(request,'sales/sales_list.html',{'product':product,'query':query})

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
    product=Product.objects.all()
    sales=Sale.objects.all()
    customer=Customer.objects.all()
    supplier=Supplier.objects.all()
    purchase=Purchase.objects.all()
    #Counting of each models items
    prod_count=product.count()
    sales_count=sales.count()
    customer_count=customer.count()
    supplier_count=supplier.count()
    purchase_count=purchase.count()

    # counting total prices of all quantity of individual model

    total_product = Product.objects.aggregate(total=Sum('quantity'))['total'] or 0
    total_sales = Sale.objects.aggregate(
    total=Sum(F('quantity') * F('sale_price'), output_field=FloatField())
)['total'] or 0
    #recent orders
    salesByDate = Sale.objects.all().order_by('-sale_date')[:3]
    #top selling producst
    topSelling=Sale.objects.all().order_by('-quantity')[:3]
    #out of stock products
    outOfStock=Product.objects.filter(quantity=0)
    #low stock product
    lowStockProducts = Product.objects.filter(quantity__lt=10).order_by('quantity')
    return render(request,'dashboard/index.html',{'product':product,'prod_count':prod_count,'outOfStock':outOfStock,'lowStockProducts':lowStockProducts,
                                                  'sales':sales,'sales_count':sales_count,'salesByDate': salesByDate,'topSelling':topSelling,
                                                  'customer':customer,'customer_count':customer_count,
                                                  'supplier':supplier,'supplier_count':supplier_count,
                                                  'purchase':purchase,'purchase_count':purchase_count})

#view for recent order or recent sold products
