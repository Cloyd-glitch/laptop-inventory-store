from django.urls import path
from . import views

app_name = 'staff_panel'

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    
    # Catalog
    path('catalog/laptops/', views.laptop_list, name='laptop_list'),
    path('catalog/laptops/create/', views.laptop_create, name='laptop_create'),
    path('catalog/laptops/<int:pk>/edit/', views.laptop_update, name='laptop_update'),
    path('catalog/laptops/<int:pk>/delete/', views.laptop_delete, name='laptop_delete'),
    
    # Orders
    path('orders/', views.order_list, name='order_list'),
    path('orders/<int:pk>/', views.order_detail, name='order_detail'),
    
    # Bookings
    path('bookings/', views.booking_list, name='booking_list'),
    path('bookings/<int:pk>/', views.booking_detail, name='booking_detail'),
    
    # Payments
    path('payments/', views.payment_list, name='payment_list'),
    path('payments/<int:pk>/verify/', views.payment_verify, name='payment_verify'),
    
    # Accounts
    path('accounts/users/', views.user_list, name='user_list'),
    path('accounts/users/<int:pk>/', views.user_detail, name='user_detail'),
    path('accounts/users/<int:pk>/edit/', views.user_update, name='user_update'),
    path('accounts/users/<int:pk>/delete/', views.user_delete, name='user_delete'),
]
