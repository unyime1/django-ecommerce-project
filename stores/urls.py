from django.urls import path


from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('store/', views.store, name='store'),
    path('checkout/', views.checkout, name='checkout'),
    path('contact/', views.contact, name='contact'),
    path('cart/', views.cart, name='cart'),

    path('update_item/', views.updateItem, name='update_item'),
    path('process_order/', views.processOrder, name='process_order'),
    path('order/<str:order_id>/', views.orderDetailsPage, name='order'),
    path('product/<str:product_id>/', views.productPage, name='product'),
    
] 