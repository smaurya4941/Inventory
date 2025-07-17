from django.shortcuts import render,redirect,get_object_or_404
from inventory.models import Customer
from .forms import UserRegistrationForm
from django.contrib.auth import login,logout,user_logged_in
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
