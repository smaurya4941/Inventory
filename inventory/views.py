from django.shortcuts import render,redirect,get_object_or_404
from .models import Product,Customer,Purchase
from .forms import ProductForm

# Create your views here.


#view to add product\\

def view_product(request):
    products=Product.objects.all()
    return render(request,'view_product.html',{'products':products})


def add_product(request):
    if request.method=='POST':
        form=ProductForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('product_list')
    else:
        form=ProductForm()
    return render(request,'add_product.html',{'form':form})

def edit_product(request,pk):
    product=get_object_or_404(Product,pk=pk)
    # print(product.name)
    form=ProductForm(request.POST or None,instance=product)
    if form.is_valid():
        form.save()
        return redirect('product_list')
    return render(request,'add_product.html',{'form':form})


def delete_product(request,pk):
    product=get_object_or_404(Product,pk=pk)
    if request.method=='POST':
        product.delete()
        return redirect('product_list')
    return render(request,'conf_delete.html',{'product':product})