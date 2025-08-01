from django.shortcuts import render,redirect,get_object_or_404
from .models import Product,Customer,Purchase,Supplier,Sale
from .forms import ProductForm,SupplierForm,PurchaseForm,SaleForm
from django.db.models import F, Sum, FloatField
from django.contrib import messages
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.core.mail import send_mail#method jiske under saara email content likhenege
from django.template.loader import render_to_string
from django.http import HttpResponse
from xhtml2pdf import pisa

# Create your views here.


#**********************ITEMS*******************************




#********************************PRODUCTS****************************
#view listed product

def view_product(request):
    if not request.user.is_authenticated:
        return redirect('first')
    query = request.GET.get('q')  #search property==>url se GET karenge ==>q
   
    products=Product.objects.all()
    #search features
    if query:
        products = products.filter(name__name__icontains=query) | products.filter(sku__icontains=query)

    #filtering
    sort=request.GET.get('sort')
    # print(sort)
    valid_sort_fields = ['name__name', '-name__name', 'price', '-price', 'quantity', '-quantity']
    if sort in valid_sort_fields:
        products=products.order_by(sort)
    
    for product in products:
        product.total_cost=product.quantity * product.price
    return render(request,'product/view_product.html',{'products':products,'query':query,'sort':sort})

#add product
@login_required
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
@login_required
def edit_product(request,pk):
    product=get_object_or_404(Product,pk=pk)
    # print(product.name)
    form=ProductForm(request.POST or None,instance=product)
    if form.is_valid():
        form.save()
        return redirect('product_list')
    return render(request,'product/add_product.html',{'form':form})


#delete product
@login_required
def delete_product(request,pk):
    product=get_object_or_404(Product,pk=pk)
    if request.method=='POST':
        product.delete()
        return redirect('product_list')
    return render(request,'product/conf_delete.html',{'product':product})





#*****************************SUPPLIER VIEWS CRUD**********************

#view listed supplier
def view_supplier(request):
    if not request.user.is_authenticated:
        return redirect('first')
    supplier=Supplier.objects.all()
    query=request.GET.get('q')
    if query:
        supplier=supplier.filter(name__icontains=query) | supplier.filter(address__icontains=query)
    
    #sorting
    sort=request.GET.get('sort')
    valid_sort_fields=['name','-name']
    if sort in valid_sort_fields:
        supplier=supplier.order_by(sort)
        
    return render(request,'supplier/view_supplier.html',{'supplier':supplier,'query':query,'sort':sort})

#add supplier
@login_required
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
@login_required
def edit_supplier(request,pk):
    supplier=get_object_or_404(Supplier,pk=pk)
    form=SupplierForm(request.POST or None,instance=supplier)
    if form.is_valid():
        form.save()
        return redirect('supplier_list')
    return render(request,'supplier/add_supplier.html',{'form':form})


#delete supplier
@login_required
def delete_supplier(request,pk):
    supplier=get_object_or_404(Supplier,pk=pk)
    if request.method=='POST':
        supplier.delete()
        return redirect('supplier_list')
    return render(request,'supplier/conf_delete_supplier.html',{'supplier':supplier})




#***********************************PURCHASE  *******************************
#list all purchased items

def purchase_list(request):
    if not request.user.is_authenticated:
        return redirect('first')
    query=request.GET.get('q')
   #search featiures
    purchases=Purchase.objects.all()
    if query:
        purchases=purchases.filter(supplier__name__icontains=query)|purchases.filter(product__name__icontains=query)

    #ordering
    valid_sort_fields=['product__name','-product__name','purchase_price','-purchase_price','quantity','-quantity']
    sort=request.GET.get('sort')
    if sort in valid_sort_fields:
        purchases=purchases.order_by(sort)
   
    return render(request,'purchase/purchase_list.html',{'query':query,'purchases':purchases,'sort':sort})
#view to purchase product/items from supplier
@login_required
def create_purchase(request):
    if request.method == 'POST':
        form = PurchaseForm(request.POST)
        if form.is_valid():
            purchase = form.save()

            # Get purchased Item and quantity
            purchased_item = purchase.product  # This is your Items model
            purchased_quantity = purchase.quantity
            purchase_price = purchase.purchase_price

            # Check if this Item exists in Product
            existing_product = Product.objects.filter(name=purchased_item).first()

            if existing_product:
                # Update quantity if Product already exists
                existing_product.quantity += purchased_quantity
                existing_product.save()
                messages.success(request, f"Stock updated for '{purchased_item.name}'.")
            else:
                # Create new Product if not exists
                Product.objects.create(
                    name=purchased_item,
                    sku=f"{purchased_item.name[:3].upper()}-{purchased_item.id}",
                    description='Auto-created from purchase',
                    price=purchase_price,
                    quantity=purchased_quantity
                )
                messages.success(request, f"New Product created for '{purchased_item.name}'.")

            return redirect('purchase_list')
    else:
        form = PurchaseForm()

    return render(request, 'purchase/purchase_product.html', {'form': form})

#edit purchase 
@login_required
def edit_purchase(request,pk):
    item=get_object_or_404(Purchase,pk=pk)
    form=PurchaseForm(request.POST or None,instance=item)
    if form.is_valid():
        form.save()
        return redirect('purchase_list')
    return render(request,'purchase/purchase_product.html',{'form':form})


#delete Purchase
@login_required
def delete_purchase(request,pk):
    item=get_object_or_404(Purchase,pk=pk)
    if request.method=='POST':
        item.delete()
        return redirect('purchase_list')
    return render(request,'purchase/conf_delete_purchase.html',{'item':item})


#*******************SALES VIEWS*************************

#list of all sales
def sales_list(request):
    if not request.user.is_authenticated:
        return redirect('first')

    query = request.GET.get('q')
    sort = request.GET.get('sort')
    sales=Sale.objects.all()

    if query:
        sales = sales.filter(customer__name__icontains=query) | sales.filter(product__name__name__icontains=query)
    else:
        sales =sales

    #filtering 
    valid_sort_fields = ['product__name__name', '-product__name__name', 'sale_price', '-sale_price', 'quantity', '-quantity']
    if sort in valid_sort_fields:
        sales=sales.order_by(sort)
    else:
        sales=sales
    
    return render(request,'sales/sales_list.html',{'sales':sales,'query':query,'sort':sort})
#create_sales
@login_required
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
                return redirect('invoice_preview',sale_id=sale.id)
            else:
                form.add_error('quantity',"Not enough items available")
    else:
        form=SaleForm()
    return render(request,'sales/sales_product.html',{'form':form})

#edit sales
@login_required
def edit_sales(request,pk):
    sales=get_object_or_404(Sale,pk=pk)
    form=SaleForm(request.POST or None,instance=sales)
    if form.is_valid():
        form.save()
        return redirect('sales_list')
    return render(request,'sales/sales_product.html',{'form':form})


#delete the sales
@login_required
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
    if not request.user.is_authenticated:  ###isse agar ek jagah se logout ho to har window me logout kr dega
        return redirect('first')

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
    topSelling = Sale.objects.values('product__name__name') \
    .annotate(total_quantity=Sum('quantity')) \
    .order_by('-total_quantity')[:3]
    # print(topSelling)
    # topSelling=Sale.objects.all().order_by('-quantity')[:3] # it gives the duplicates sales item 


    #out of stock products
    outOfStock=Product.objects.filter(quantity=0)

    
    #low stock product
    lowStockProducts = Product.objects.filter(quantity__lt=10).order_by('quantity')
    return render(request,'dashboard/index.html',{'product':product,'prod_count':prod_count,'outOfStock':outOfStock,'lowStockProducts':lowStockProducts,
                                                  'sales':sales,'sales_count':sales_count,'salesByDate': salesByDate,'topSelling':topSelling,
                                                  'customer':customer,'customer_count':customer_count,
                                                  'supplier':supplier,'supplier_count':supplier_count,
                                                  'purchase':purchase,'purchase_count':purchase_count})


def first_page(request):
    if request.method=='POST':
        name=request.POST.get('name')
        email=request.POST.get('email')
        message=request.POST.get('message')
        full_message=f'message received from {name} via {email} :\n \n{message}'

        send_mail(
            subject=f'new contact message from {name}',
            message=full_message,
            from_email=email,
            recipient_list= ['smaurya2274@gmail.com'],
            fail_silently=False,

        )

        messages.success(request,'Your email has been sent')
        return redirect('/#contact')
    return render(request,'dashboard/first.html')












#*********************DOWNLOAD INVOICE***********************


def generate_invoice_pdf(request, sale_id):
    sale = Sale.objects.get(id=sale_id)
    total_price=sale.quantity *sale.sale_price
    html = render_to_string('sales/invoice.html', {'sale': sale,'total_price':total_price})
    response = HttpResponse(content_type='application/pdf') #blank response
    response['Content-Disposition'] = f'inline; filename="invoice_{sale.id}.pdf"'
    pisa.CreatePDF(html, dest=response)
    return response

def invoice_preview(request,sale_id):
    sale = Sale.objects.get(id=sale_id)
    total_price=sale.quantity *sale.sale_price
    return render(request,'sales/invoice_preview.html',{'sale': sale,'total_price':total_price})