from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', views.home, name='home'),
    path('products/', views.products, name='products'),
    path('register/', views.registerPage,name='registerPage'),
    path('login/', views.loginPage,name='loginPage'),
    path('logout/', views.logoutUser,name='logoutPage'),

    path('reset_password/', auth_views.PasswordResetView.as_view(template_name='accounts/password_reset.html'), name='password_reset'),
    path('reset_password_sent/', auth_views.PasswordResetDoneView.as_view(template_name='accounts/password_reset_sent.html'), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name='accounts/password_reset_form.html'), name='password_reset_confirm'),
    path('reset_password_complete/', auth_views.PasswordResetCompleteView.as_view(template_name='accounts/password_reset_complete.html'), name='password_reset_complete'),
  
  
    
   

    path('user/', views.userPage,name='userPage'),
    path('account/', views.accountSettings,name='account'),


    path('customer/<str:pk_no>/', views.customer, name='customer'),
    path('create_order/<str:pk>/', views.createOrder, name='createOrder'),
    path('update_order/<str:pk>/', views.updateOrder, name='update_order'),
    path('delete_order/<str:pk>/', views.deleteOrder, name='delete_order'),
    
]


"""
1 - submit email form                           PasswordResetView.as_view()
2 - email sent succes message                   PasswordResetDoneView.as_view()
3 - Link to password Rest form in email         PasswordResetConfirmView.as_view()
4 - Password succesfully changed message        PasswordResetCompleteView.as_view()     
"""