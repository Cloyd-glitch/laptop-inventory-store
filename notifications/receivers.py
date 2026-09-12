"""
Signal receivers for the notifications app.
Imported by orders.apps.OrdersConfig.ready()
"""
from orders.signals import order_confirmed, booking_confirmed, payment_verified
from .emails import send_order_confirmation, send_booking_confirmation, send_payment_verified_email


def on_order_confirmed(sender, order, **kwargs):
    send_order_confirmation(order)


def on_booking_confirmed(sender, booking, **kwargs):
    send_booking_confirmation(booking)


def on_payment_verified(sender, payment, **kwargs):
    send_payment_verified_email(payment)


order_confirmed.connect(on_order_confirmed)
booking_confirmed.connect(on_booking_confirmed)
payment_verified.connect(on_payment_verified)
