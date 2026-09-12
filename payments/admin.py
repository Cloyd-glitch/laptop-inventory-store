from django.contrib import admin
from django.utils.html import format_html
from django.contrib import messages as django_messages
from .models import Payment
from orders.signals import payment_verified as payment_verified_signal


@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = (
        'id', 'order_link', 'customer_name', 'method', 'amount_display',
        'status_badge', 'reference_number', 'paid_at', 'created_at'
    )
    list_filter = ('status', 'method', 'created_at')
    search_fields = ('order__id', 'order__customer__username', 'reference_number')
    readonly_fields = ('created_at', 'updated_at', 'paid_at')
    ordering = ('-created_at',)
    actions = ['verify_payments']

    def order_link(self, obj):
        return format_html('<a href="/admin/orders/order/{}/change/">Order #{}</a>', obj.order_id, obj.order_id)
    order_link.short_description = "Order"

    def customer_name(self, obj):
        return obj.order.customer.username
    customer_name.short_description = "Customer"

    def amount_display(self, obj):
        return format_html('<strong>₱{}</strong>', f"{obj.amount:,.2f}")
    amount_display.short_description = "Amount"

    def status_badge(self, obj):
        colors = {
            'PENDING': '#c98a4b',
            'VERIFIED': '#5a9e6f',
            'FAILED': '#b85450',
            'REFUNDED': '#6b7280',
        }
        color = colors.get(obj.status, '#888')
        return format_html(
            '<span style="background:{};color:#fff;padding:2px 8px;border-radius:12px;font-size:11px;">{}</span>',
            color, obj.get_status_display()
        )
    status_badge.short_description = "Status"

    @admin.action(description="✓ Verify selected payments")
    def verify_payments(self, request, queryset):
        verified = 0
        for payment in queryset.filter(status=Payment.Status.PENDING):
            payment.verify()
            payment_verified_signal.send(sender=Payment, payment=payment)
            verified += 1
        self.message_user(request, f"{verified} payment(s) verified.", django_messages.SUCCESS)
