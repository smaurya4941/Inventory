from django.urls import path,include
from .views import view_customer
urlpatterns = [
    path('',view_customer,name='view_customer'),
]
