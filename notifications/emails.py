from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.conf import settings


def send_order_confirmation(order):
    """Send order confirmation email to the customer."""
    subject = f"✅ Order #{order.pk} Confirmed — LaptopStore"
    html_message = render_to_string('notifications/email/order_confirmation.html', {'order': order})
    plain_message = (
        f"Hi {order.customer.username},\n\n"
        f"Your order #{order.pk} has been placed successfully.\n"
        f"Total: ₱{order.total_amount:,.2f}\n\n"
        "We'll notify you when it ships.\n\n"
        "— LaptopStore Team"
    )
    send_mail(
        subject=subject,
        message=plain_message,
        from_email=settings.DEFAULT_FROM_EMAIL,
        recipient_list=[order.customer.email],
        html_message=html_message,
        fail_silently=True,
    )
    # Also alert admin
    send_mail(
        subject=f"[Admin] New Order #{order.pk} from {order.customer.username}",
        message=f"Order #{order.pk} — Total ₱{order.total_amount:,.2f}\nCustomer: {order.customer.email}",
        from_email=settings.DEFAULT_FROM_EMAIL,
        recipient_list=[settings.ADMIN_EMAIL],
        fail_silently=True,
    )


def send_booking_confirmation(booking):
    """Send booking confirmation email to the customer."""
    subject = f"📋 Booking #{booking.pk} Confirmed — LaptopStore"
    html_message = render_to_string('notifications/email/booking_confirmation.html', {'booking': booking})
    plain_message = (
        f"Hi {booking.customer.username},\n\n"
        f"Your booking for {booking.laptop} has been confirmed.\n"
        f"Unit reserved until: {booking.expires_at.strftime('%B %d, %Y')}.\n\n"
        "Please complete your purchase before the expiry date.\n\n"
        "— LaptopStore Team"
    )
    send_mail(
        subject=subject,
        message=plain_message,
        from_email=settings.DEFAULT_FROM_EMAIL,
        recipient_list=[booking.customer.email],
        html_message=html_message,
        fail_silently=True,
    )


def send_payment_verified_email(payment):
    """Notify customer that their payment was verified."""
    subject = f"💳 Payment Verified — Order #{payment.order_id} — LaptopStore"
    html_message = render_to_string('notifications/email/payment_verified.html', {'payment': payment})
    plain_message = (
        f"Hi {payment.order.customer.username},\n\n"
        f"Your payment of ₱{payment.amount:,.2f} for Order #{payment.order_id} has been verified.\n"
        "Your order is now being processed.\n\n"
        "— LaptopStore Team"
    )
    send_mail(
        subject=subject,
        message=plain_message,
        from_email=settings.DEFAULT_FROM_EMAIL,
        recipient_list=[payment.order.customer.email],
        html_message=html_message,
        fail_silently=True,
    )
