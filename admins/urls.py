from django.urls import path

from . import views


urlpatterns = [

    path('panel/', views.adminPanel, name='panel'),
    path('update_status/<str:order_id>/', views.updateOrderStatus, name='update_status'),
    path('full_orders/', views.fullOrderPage, name='full_orders'),
    path('add_products/', views.addProducts, name='add_products'),
    path('delete_products/<str:product_id>/', views.deleteProduct, name='delete_products'),
    path('update_product/<str:product_id>/', views.updateProduct, name='update_product'),

]