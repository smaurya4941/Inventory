from django.urls import path,include
from .views import view_customer,registerUser,add_customer,edit_customer,delete_customer,send_email,activate,admin_dashboard,customer_dashboard,staff_dashboard
from django.contrib.auth import views as auth_views

urlpatterns = [
    #*************customer*******************
    path('customer/',view_customer,name='view_customer'),
    path('add_customer/',add_customer,name='add_customer'),
    path('<int:pk>/edit_customer/',edit_customer,name='edit_customer'),
    path('<int:pk>/delete_customer/',delete_customer,name='delete_customer'),

    #**************AUTHENTICATIOON   ***************
    path('register/',registerUser,name="register"),
    path('login/',auth_views.LoginView.as_view(template_name='authentication/login.html'),name='login'),
    path('logout/',auth_views.LogoutView.as_view(next_page='first'),name='logout'),

    #****************EMAIL AUTHWNTOCATION AND AUTHORISATION***************************#
    path('send_email/',send_email,name='send_email'), #for console based 
    path('activate/<uidb64>/<token>/',activate,name='activate'),

    #*************************RESET PASSWORD *********************************#
    # Note instead of explicitely mentioning the template name we can skip this step but template name shuold be in correct path and correct name as django ask
    # Note: If you don't specify template_name, Django will search for the default paths.
    # Here you are giving custom templates, so extension .html is mandatory.
    path('password/reset_password/',auth_views.PasswordResetView.as_view(template_name='password/password_reset_form.html'),name='password_reset'),
    path('password/reset_done/',auth_views.PasswordResetDoneView.as_view(template_name='password/password_reset_done.html'),name='password_reset_done'),
    path('password/<uidb64>/<token>/',auth_views.PasswordResetConfirmView.as_view(template_name='password/password_reset_confirm.html'),name='password_reset_confirm'),
    path('password/reset_complete/',auth_views.PasswordResetCompleteView.as_view(template_name='password/password_reset_complete.html'),name='password_reset_complete'),

    #***********CONTACT ME PAGE *********************************
    # path('contact/',)




    #***************DASHBOARD ***********
    path('admin_dashboard/',admin_dashboard,name='admin_dashboard'),
    path('customer_dashboard/',customer_dashboard,name='customer_dashboard'),
    path('staff_dashboard/',staff_dashboard,name='staff_dashboard'),
]
