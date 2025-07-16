from django.shortcuts import render,redirect,get_object_or_404
from inventory.models import Customer
# Create your views here.

#******************CUSTOMER***************
def view_customer(request):
    customer=Customer.objects.all()
    return render(request,'customer/view_customer.html',{'customer':customer})
