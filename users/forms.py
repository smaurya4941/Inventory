from django.contrib.auth.models import User
from django import forms
from django.contrib.auth.forms import UserCreationForm
from inventory.models import Customer

#to register new User/Admin
class UserRegistrationForm(UserCreationForm):
    email=forms.EmailField()
    class Meta:
        model=User
        fields=('username','email','password1','password2')

    def __init__(self, *args, **kwargs):
        super(UserRegistrationForm, self).__init__(*args, **kwargs)
        self.fields['username'].help_text=None
        self.fields['password1'].help_text = None
        self.fields['password2'].help_text = None


#create new customer
class AddCustomer(forms.ModelForm):
    class Meta:
        model=Customer
        fields='__all__'
        widgets = {
                    'address': forms.Textarea(attrs={'rows': 4,  'cols': 40,  'placeholder': 'Add Address  here...'}),
                    'email':forms.EmailInput(attrs={ 'placeholder': 'Enter your email  here...'  }),
        }
