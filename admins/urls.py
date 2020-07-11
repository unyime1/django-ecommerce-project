from django.urls import path

from . import views


urlpatterns = [

    path('panel/', views.adminPanel, name='panel'),

]