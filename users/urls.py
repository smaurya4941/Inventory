from django.urls import path,include
from .views import view_customer,registerUser,add_customer,edit_customer,delete_customer
from django.contrib.auth import views as auth_views
urlpatterns = [
    #*************customer*******************
    path('customer/',view_customer,name='view_customer'),
    path('add_customer/',add_customer,name='add_customer'),
    path('<int:pk>/edit_customer/',edit_customer,name='edit_customer'),
    path('<int:pk>/delete_customer/',delete_customer,name='delete_customer'),
    path('register/',registerUser,name="register"),
    path('login/',auth_views.LoginView.as_view(template_name='authentication/login.html'),name='login'),
    path('logout/',auth_views.LogoutView.as_view(next_page='dashboard'),name='logout'),
]
