from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.views.decorators.http import require_POST

from catalog.models import Laptop
from .cart import Cart
from .models import Order, OrderItem, Booking
from .signals import order_confirmed, booking_confirmed


# ────────────────────────────────────────────
#  Cart views
# ────────────────────────────────────────────

def cart_view(request):
    cart = Cart(request)
    return render(request, 'orders/cart.html', {'cart': cart})


@require_POST
def add_to_cart(request, laptop_id):
    laptop = get_object_or_404(Laptop, pk=laptop_id, is_active=True)
    cart = Cart(request)
    quantity = int(request.POST.get('quantity', 1))
    if quantity < 1:
        quantity = 1
    if quantity > laptop.stock_quantity:
        messages.warning(request, f"Only {laptop.stock_quantity} unit(s) available.")
        quantity = laptop.stock_quantity
    cart.add(laptop, quantity=quantity)
    messages.success(request, f"{laptop.brand} {laptop.model_name} added to cart.")
    next_url = request.POST.get('next', 'orders:cart')
    return redirect(next_url)


@require_POST
def remove_from_cart(request, laptop_id):
    cart = Cart(request)
    cart.remove(laptop_id)
    messages.info(request, "Item removed from cart.")
    return redirect('orders:cart')


@require_POST
def update_cart(request, laptop_id):
    cart = Cart(request)
    quantity = int(request.POST.get('quantity', 1))
    cart.update(laptop_id, quantity)
    return redirect('orders:cart')


# ────────────────────────────────────────────
#  Checkout & Order views
# ────────────────────────────────────────────

@login_required
def checkout_view(request):
    cart = Cart(request)
    if len(cart) == 0:
        messages.warning(request, "Your cart is empty.")
        return redirect('orders:cart')

    # Pre-fill address from profile
    initial_address = request.user.address or ''

    if request.method == 'POST':
        shipping_address = request.POST.get('shipping_address', '').strip()
        notes = request.POST.get('notes', '').strip()
        if not shipping_address:
            messages.error(request, "Please provide a shipping address.")
            return render(request, 'orders/checkout.html', {
                'cart': cart,
                'initial_address': initial_address,
            })

        # Validate stock for all items
        stock_errors = []
        for item in cart:
            laptop = item.get('laptop')
            if laptop and item['quantity'] > laptop.stock_quantity:
                stock_errors.append(
                    f"{laptop.brand} {laptop.model_name}: only {laptop.stock_quantity} left."
                )
        if stock_errors:
            for err in stock_errors:
                messages.error(request, err)
            return render(request, 'orders/checkout.html', {
                'cart': cart,
                'initial_address': initial_address,
            })

        # Create Order
        order = Order.objects.create(
            customer=request.user,
            shipping_address=shipping_address,
            notes=notes,
        )
        for item in cart:
            laptop = item.get('laptop')
            if laptop:
                OrderItem.objects.create(
                    order=order,
                    laptop=laptop,
                    quantity=item['quantity'],
                    unit_price=item['price'],
                )
                # Decrement stock
                laptop.stock_quantity -= item['quantity']
                laptop.save(update_fields=['stock_quantity'])

        order.compute_total()
        cart.clear()

        # Fire signal → email notification
        order_confirmed.send(sender=Order, order=order)

        messages.success(request, f"Order #{order.pk} placed successfully!")
        return redirect('orders:order_confirm', pk=order.pk)

    return render(request, 'orders/checkout.html', {
        'cart': cart,
        'initial_address': initial_address,
    })


@login_required
def order_confirm_view(request, pk):
    order = get_object_or_404(Order, pk=pk, customer=request.user)
    return render(request, 'orders/confirm.html', {'order': order})


@login_required
def order_detail_view(request, pk):
    order = get_object_or_404(Order, pk=pk, customer=request.user)
    return render(request, 'orders/order_detail.html', {'order': order})


# ────────────────────────────────────────────
#  Booking views
# ────────────────────────────────────────────

@login_required
def booking_create_view(request, laptop_id):
    laptop = get_object_or_404(Laptop, pk=laptop_id, is_active=True)

    if not laptop.in_stock:
        messages.error(request, "Sorry, this laptop is currently out of stock.")
        return redirect('catalog:detail', slug=laptop.slug)

    if request.method == 'POST':
        notes = request.POST.get('notes', '').strip()
        booking = Booking.objects.create(
            customer=request.user,
            laptop=laptop,
            quantity=1,
            notes=notes,
            status=Booking.Status.CONFIRMED,
        )
        # Hold 1 unit
        laptop.stock_quantity -= 1
        laptop.save(update_fields=['stock_quantity'])

        booking_confirmed.send(sender=Booking, booking=booking)

        messages.success(
            request,
            f"Booking #{booking.pk} confirmed! Unit reserved for {booking.expires_at.strftime('%b %d, %Y')}."
        )
        return redirect('accounts:my_bookings')

    return render(request, 'orders/booking_create.html', {'laptop': laptop})


@login_required
def booking_detail_view(request, pk):
    booking = get_object_or_404(Booking, pk=pk, customer=request.user)
    return render(request, 'orders/booking_detail.html', {'booking': booking})


@login_required
def booking_cancel_view(request, pk):
    booking = get_object_or_404(Booking, pk=pk, customer=request.user)
    if request.method == 'POST':
        if booking.status in (Booking.Status.PENDING, Booking.Status.CONFIRMED):
            booking.status = Booking.Status.CANCELLED
            booking.save(update_fields=['status'])
            # Return unit to stock
            booking.laptop.stock_quantity += booking.quantity
            booking.laptop.save(update_fields=['stock_quantity'])
            messages.success(request, "Booking cancelled and stock restored.")
        else:
            messages.error(request, "This booking cannot be cancelled.")
        return redirect('accounts:my_bookings')
    return render(request, 'orders/booking_cancel_confirm.html', {'booking': booking})
