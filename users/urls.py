from django.urls import path
from django.contrib.auth import views as auth_views

from . import views

urlpatterns = [
    path('profile/', views.userProfile, name='profile'),
    path('register/', views.userRegistration, name='register'),
    path('login/', views.userLogin, name='login'),
    path('logout/', views.userLogout, name='logout'),
  
    
    #password reset views
      path('password_reset/', auth_views.PasswordResetView.as_view(
        ),
        name='password_reset'), #template_name="accounts/password_reset.html"
    path('password_reset_sent/', auth_views.PasswordResetDoneView.as_view(
        ),
        name='password_reset_done'), #template_name="accounts/password_reset_sent.html"
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(
        ),
        name='password_reset_confirm'), #template_name="accounts/password_reset_form.html"
    path('password_reset_complete/', auth_views.PasswordResetCompleteView.as_view(
        ),
        name='password_reset_complete'),    #template_name="accounts/password_reset_done.html"

        #send email view

    path('activate/<uidb64>/<token>/', views.activateAccount, name='activate'),
]

"""
1. Submit email     PasswordResetView.as_view()
2. email sent success message   PasswordResetDoneView.as_view()
3. link to password reset form  PasswordResetConfirmView.as_view()
4. password successfully changed message    PasswordResetCompleteView.as_view()
"""