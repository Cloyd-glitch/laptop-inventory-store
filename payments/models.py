from django.db import models
from django.utils import timezone
from orders.models import Order


class Payment(models.Model):
    class Method(models.TextChoices):
        COD = 'COD', 'Cash on Delivery'
        BANK_TRANSFER = 'BANK', 'Bank Transfer'
        GCASH = 'GCASH', 'GCash'
        CREDIT_CARD = 'CARD', 'Credit / Debit Card'

    class Status(models.TextChoices):
        PENDING = 'PENDING', 'Pending'
        VERIFIED = 'VERIFIED', 'Verified'
        FAILED = 'FAILED', 'Failed'
        REFUNDED = 'REFUNDED', 'Refunded'

    order = models.OneToOneField(Order, on_delete=models.CASCADE, related_name='payment')
    method = models.CharField(max_length=10, choices=Method.choices, default=Method.COD)
    status = models.CharField(max_length=10, choices=Status.choices, default=Status.PENDING)
    reference_number = models.CharField(
        max_length=100, blank=True,
        help_text="Bank ref number, GCash ref, or transaction ID"
    )
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    paid_at = models.DateTimeField(null=True, blank=True)
    notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def verify(self):
        """Mark payment as verified and record timestamp."""
        self.status = self.Status.VERIFIED
        self.paid_at = timezone.now()
        self.save(update_fields=['status', 'paid_at'])
        # Advance order to processing
        self.order.status = 'PROCESSING'
        self.order.save(update_fields=['status'])

    def __str__(self):
        return f"Payment #{self.pk} — Order #{self.order_id} [{self.get_status_display()}]"
