from django.urls import path,include
from .views import view_customer,registerUser
from django.contrib.auth import views as auth_views
urlpatterns = [
    path('',view_customer,name='view_customer'),
    path('register/',registerUser,name="register"),
    path('login/',auth_views.LoginView.as_view(template_name='authentication/login.html'),name='login'),
    path('logout/',auth_views.LogoutView.as_view(next_page='dashboard'),name='logout'),
]
