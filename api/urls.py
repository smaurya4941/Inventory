from . import views
from django.urls import path,include
from rest_framework.routers import DefaultRouter

router=DefaultRouter()
router.register('productapi',views.ProductViewsets,basename='productapi')
router.register('customerapi',views.CustomerViewsets,basename='customerapi')
router.register('salesapi',views.SaleViewsets,basename='salesapi')
router.register('purchaseapi',views.PurchaseViewsets,basename='purchaseapi')
router.register('supplierapi',views.SupplierViewsets,basename='supplierapi')
router.register('userapi',views.UserViewsets,basename='userapi')



urlpatterns=[
   path('',include(router.urls)),
   path('auth/',include('rest_framework.urls',namespace='rest_framework')), #for manual login logout
]

