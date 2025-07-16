from inventory import urls as inventory_url
from django.contrib import admin
from django.urls import path,include
from users import urls as users_url
urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include(inventory_url)),
    path('users/',include(users_url)),
]
