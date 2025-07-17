from django.shortcuts import render,redirect,get_object_or_404
from inventory.models import Customer
from .forms import UserRegistrationForm
from django.contrib.auth import login,logout,user_logged_in
from django.contrib.auth.decorators import login_required
from .forms import AddCustomer
# Create your views here.

#******************CUSTOMER***************
def view_customer(request):
    customer=Customer.objects.all()
    return render(request,'customer/view_customer.html',{'customer':customer})

def registerUser(request):
    if request.method=='POST':
        form =UserRegistrationForm(request.POST)
        if form.is_valid():
            user=form.save()
            login(request,user)
            return redirect('dashboard')
    else:
        form=UserRegistrationForm()
    return render(request,'authentication/registration.html',{'form':form})

@login_required
def add_customer(request):
    if request.method=='POST':
        form=AddCustomer(request.POST)
        if form.is_valid():
            form.save()
            return redirect('view_customer')
    else :
        form=AddCustomer()
    return render(request,'customer/add_customer.html',{'form':form})

@login_required
def edit_customer(request,pk):
    customer=get_object_or_404(Customer,pk=pk)#accessing product with pk=pk
    if request.method=='POST':
        form=AddCustomer(request.POST or None,instance=customer)
        if form.is_valid():
            form.save()
            return redirect('view_customer')
    else:
        form=AddCustomer(instance=customer)
    return render(request,'customer/add_customer.html',{'form':form})



@login_required
def delete_customer(request,pk):
    customer=get_object_or_404(Customer,pk=pk)
    if request.method=='POST':
        customer.delete()
        return redirect('view_customer')
    return render(request,'customer/conf_delete_customer.html',{'customer':customer})

