from django.urls import path

from . import views


urlpatterns = [

    path('panel/', views.adminPanel, name='panel'),
    path('update_status/<str:order_id>/', views.updateOrderStatus, name='update_status'),
    

]