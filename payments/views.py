from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.views.decorators.http import require_POST

from orders.models import Order
from orders.signals import payment_verified as payment_verified_signal
from .models import Payment


@login_required
def payment_create_view(request, order_id):
    order = get_object_or_404(Order, pk=order_id, customer=request.user)

    # Prevent duplicate payments
    if hasattr(order, 'payment'):
        messages.info(request, "Payment already submitted for this order.")
        return redirect('payments:status', payment_id=order.payment.pk)

    if request.method == 'POST':
        method = request.POST.get('method', Payment.Method.COD)
        reference_number = request.POST.get('reference_number', '').strip()
        notes = request.POST.get('notes', '').strip()

        payment = Payment.objects.create(
            order=order,
            method=method,
            amount=order.total_amount,
            reference_number=reference_number,
            notes=notes,
        )
        messages.success(
            request,
            f"Payment submitted! Reference: {reference_number or 'N/A'}. "
            "We'll verify and notify you by email."
        )
        return redirect('payments:status', payment_id=payment.pk)

    return render(request, 'payments/pay.html', {
        'order': order,
        'methods': Payment.Method.choices,
    })


@login_required
def payment_status_view(request, payment_id):
    payment = get_object_or_404(Payment, pk=payment_id, order__customer=request.user)
    return render(request, 'payments/status.html', {'payment': payment})
