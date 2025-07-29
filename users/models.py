from django.db import models
from django.contrib.auth.models import User
# Create your models here.

#Creating model for logins

class UserProfile(models.Model):
    ROLE_CHOICES=(
        ('admin','admin'),
        ('staff','staff'),
        ('customer','customer'),
        
    )
    user=models.OneToOneField(User,on_delete=models.CASCADE)
    role=models.CharField(max_length=20,choices=ROLE_CHOICES)

    def __str__(self):
        return f' {self.user.username}-{self.role}'
