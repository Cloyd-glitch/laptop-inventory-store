from django.dispatch import Signal

# Fired after an order is placed (cart → Order + OrderItems committed)
order_confirmed = Signal()

# Fired when a booking is created/confirmed
booking_confirmed = Signal()

# Fired when admin verifies a payment
payment_verified = Signal()
