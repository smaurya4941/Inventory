from django.db.models.signals import post_save
from django.contrib.auth.models import User
from .models import UserProfile
from django.dispatch import receiver

#Creating signal to create profile automatically when new user is registered

@receiver(post_save,sender=User)
def create_user_profile(sender,instance,created,**kwargs):
    if created:
        UserProfile.objects.create(user=instance)