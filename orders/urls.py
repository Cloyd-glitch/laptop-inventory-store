from django.urls import path
from . import views

app_name = 'orders'

urlpatterns = [
    # Cart
    path('cart/', views.cart_view, name='cart'),
    path('cart/add/<int:laptop_id>/', views.add_to_cart, name='add_to_cart'),
    path('cart/remove/<int:laptop_id>/', views.remove_from_cart, name='remove_from_cart'),
    path('cart/update/<int:laptop_id>/', views.update_cart, name='update_cart'),

    # Checkout & Orders
    path('checkout/', views.checkout_view, name='checkout'),
    path('orders/<int:pk>/', views.order_detail_view, name='order_detail'),
    path('orders/<int:pk>/confirm/', views.order_confirm_view, name='order_confirm'),

    # Bookings
    path('bookings/create/<int:laptop_id>/', views.booking_create_view, name='booking_create'),
    path('bookings/<int:pk>/', views.booking_detail_view, name='booking_detail'),
    path('bookings/<int:pk>/cancel/', views.booking_cancel_view, name='booking_cancel'),
]
