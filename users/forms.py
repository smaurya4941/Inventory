from django.contrib.auth.models import User
from django import forms
from django.contrib.auth.forms import UserCreationForm
from inventory.models import Customer
from .models import UserProfile
#to register new User/Admin
class UserRegistrationForm(UserCreationForm):
    email=forms.EmailField()
    role=forms.ChoiceField(choices=UserProfile.ROLE_CHOICES)
    class Meta:
        model=User
        fields=('username','email','password1','password2','role')

    def __init__(self, *args, **kwargs):
        super(UserRegistrationForm, self).__init__(*args, **kwargs)
        self.fields['username'].help_text=None
        self.fields['password1'].help_text = None
        self.fields['password2'].help_text = None

    def save(self,commit=True):
        user=super().save(commit=False)
        user.email=self.cleaned_data['email']
        if commit:
            user.save()
            role=self.cleaned_data['role']
            UserProfile.objects.create(user=user,role=role)

            if role == 'customer':
                try:
                    Customer.objects.create(user=user, name=user.username, email=user.email)
                except Exception as e:
                    print("Failed to create customer:", e)
        return user


#create new customer
class AddCustomer(forms.ModelForm):
    class Meta:
        model=Customer
        fields='__all__'
        widgets = {
                    'address': forms.Textarea(attrs={'rows': 4,  'cols': 40,  'placeholder': 'Add Address  here...'}),
                    'email':forms.EmailInput(attrs={ 'placeholder': 'Enter your email  here...'  }),
        }
