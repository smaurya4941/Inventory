from django.shortcuts import render,redirect,get_object_or_404
from inventory.models import Customer
from django.http import HttpResponse
from .forms import UserRegistrationForm
from django.contrib.auth import login,logout,user_logged_in
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail,EmailMultiAlternatives
from django.contrib.auth.models import User
from django.utils.http import urlsafe_base64_decode,urlsafe_base64_encode
from django.utils.encoding import force_bytes,force_str
from django.contrib.auth.tokens import default_token_generator as token_generator
from django.urls import reverse
from .forms import AddCustomer
from .decorators import role_required
# Create your views here.

#******************CUSTOMER***************
def view_customer(request):
    if not request.user.is_authenticated:
        return redirect('first')
    
    customer=Customer.objects.all()
    #search feature
    query=request.GET.get('q')
    if query:
        customer=customer.filter(name__icontains=query)
    
    #sort
    sort=request.GET.get('sort')
    valid_sort_fields=['name','-name']
    if sort in valid_sort_fields:
        customer=customer.order_by(sort)
    return render(request,'customer/view_customer.html',{'customer':customer,'query':query,'sort':sort})

def registerUser(request):
    if request.method=='POST':
        form =UserRegistrationForm(request.POST)
        if form.is_valid():
            user=form.save(commit=False)
            user.is_active=False ##inactive rhega jbtk emailverify n ho jaaye
            # login(request,user)
            # return redirect('dashboard')
            user.save()
            #gengerating token for user
            uid=urlsafe_base64_encode(force_bytes(user.pk))
            token=token_generator.make_token(user)

            #verification link
            verification_link=request.build_absolute_uri(
                reverse('activate',kwargs={'uidb64':uid,'token':token})
            )


            #console based testing k liye
            # send_mail(
            #     'verify your Email',
            #     f'CLick here to verify Your account:\n\n{verification_link}',
            #     'inventory@gmail.com',
            #     [user.email],
            #     fail_silently=False
            # )


            #SMTP ka use krke
            subject='Verify your Email to Activate Account'
            from_email='InventoryPro smaurya2274@gmail.com'
            to_email=user.email
            text_content=f'please verify your account by cliking on this link:\n{verification_link}'


            html_content=f'''
                <h2>Welcome {user.username}!</h2>
                <p> Click below to verify your email</p>
                <a href="{verification_link}" style="padding:10px 15px;background:#4CAF50;color:white;text-decoration:none;">Verify Email</a>
            '''

            email=EmailMultiAlternatives(subject,text_content,from_email,[to_email])
            email.attach_alternative(html_content,'text/html')
            email.send()
            return render(request,'authentication/mail_sent.html')
    else:
        form=UserRegistrationForm()
    return render(request,'authentication/registration.html',{'form':form})


def activate(request,uidb64,token):
    try:
        uid=force_str(urlsafe_base64_decode(uidb64))
        user=User.objects.get(pk=uid)
    except (TypeError,ValueError,OverflowError,User.DoesNotExist):
        user=None

    if user is not  None and token_generator.check_token(user,token):
        user.is_active=True
        user.save()
        return render(request,'authentication/activation_success.html')
    else:
        return HttpResponse("Link Invalid or expired")

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


#EMAIL AUTHENTICATION
#how to sent email ==> for cosole based only
def send_email(request):
    if request.method=='POST':
        send_mail(
            subject='welcome bby!,Verify your email',
            message='your verification link is: ...',
            from_email='inventoryapp@gmail.com',
            recipient_list=['test@exapmle.com'],
            fail_silently=False,
        )
        return render(request,'authentication/mail_sent.html')
    return render(request,'authentication/send_email.html')





#CONTACT ME
def contact_me(request):
    return render(request,'contact/contactme')


#dashboard


# @role_required('admin')
def admin_dashboard(request):
    return render(request, 'userdashboard/admin_dashboard.html')

# @role_required('staff')
def staff_dashboard(request):
    return render(request, 'userdashboard/staff_dashboard.html')

# @role_required('customer')
def customer_dashboard(request):
    return render(request, 'userdashboard/customer_dashboard.html')