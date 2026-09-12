from django.urls import path
from . import views

app_name = 'payments'

urlpatterns = [
    path('<int:order_id>/pay/', views.payment_create_view, name='pay'),
    path('status/<int:payment_id>/', views.payment_status_view, name='status'),
]
