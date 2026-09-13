from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.db.models import Count, Sum
from django.utils import timezone
from .decorators import staff_required
from .forms import LaptopAdminForm, CategoryAdminForm, OrderStatusForm, BookingStatusForm, UserAdminForm
from catalog.models import Laptop, Category
from orders.models import Order, Booking
from payments.models import Payment
from accounts.models import User

@staff_required
def dashboard(request):
    """Main staff dashboard with key metrics."""
    context = {
        'total_orders': Order.objects.count(),
        'pending_orders': Order.objects.filter(status='PENDING').count(),
        'total_bookings': Booking.objects.count(),
        'active_bookings': Booking.objects.filter(status__in=['PENDING', 'CONFIRMED']).count(),
        'total_revenue': Order.objects.filter(status='COMPLETED').aggregate(Sum('total_amount'))['total_amount__sum'] or 0,
        'recent_orders': Order.objects.order_by('-created_at')[:5],
        'recent_bookings': Booking.objects.order_by('-created_at')[:5],
        'pending_payments': Payment.objects.filter(status='PENDING').count(),
    }
    return render(request, 'staff_panel/dashboard.html', context)

# --- CATALOG VIEWS ---
@staff_required
def laptop_list(request):
    laptops = Laptop.objects.all().order_by('-created_at')
    return render(request, 'staff_panel/catalog/laptop_list.html', {'laptops': laptops})

@staff_required
def laptop_create(request):
    if request.method == 'POST':
        form = LaptopAdminForm(request.POST, request.FILES)
        if form.is_valid():
            laptop = form.save()
            messages.success(request, f"Laptop '{laptop.model_name}' created successfully.")
            return redirect('staff_panel:laptop_list')
    else:
        form = LaptopAdminForm()
    return render(request, 'staff_panel/catalog/laptop_form.html', {'form': form, 'title': 'Add New Laptop'})

@staff_required
def laptop_update(request, pk):
    laptop = get_object_or_404(Laptop, pk=pk)
    if request.method == 'POST':
        form = LaptopAdminForm(request.POST, request.FILES, instance=laptop)
        if form.is_valid():
            form.save()
            messages.success(request, f"Laptop '{laptop.model_name}' updated successfully.")
            return redirect('staff_panel:laptop_list')
    else:
        form = LaptopAdminForm(instance=laptop)
    return render(request, 'staff_panel/catalog/laptop_form.html', {'form': form, 'title': f'Edit {laptop.model_name}', 'laptop': laptop})

@staff_required
def laptop_delete(request, pk):
    laptop = get_object_or_404(Laptop, pk=pk)
    if request.method == 'POST':
        laptop.delete()
        messages.success(request, "Laptop deleted.")
        return redirect('staff_panel:laptop_list')
    return render(request, 'staff_panel/confirm_delete.html', {'object_name': f"Laptop: {laptop.brand} {laptop.model_name}", 'cancel_url': 'staff_panel:laptop_list'})

# --- ORDERS VIEWS ---
@staff_required
def order_list(request):
    orders = Order.objects.all().order_by('-created_at')
    return render(request, 'staff_panel/orders/order_list.html', {'orders': orders})

@staff_required
def order_detail(request, pk):
    order = get_object_or_404(Order, pk=pk)
    if request.method == 'POST':
        form = OrderStatusForm(request.POST, instance=order)
        if form.is_valid():
            form.save()
            messages.success(request, f"Order #{order.pk} status updated.")
            return redirect('staff_panel:order_detail', pk=order.pk)
    else:
        form = OrderStatusForm(instance=order)
    return render(request, 'staff_panel/orders/order_detail.html', {'order': order, 'form': form})

# --- BOOKINGS VIEWS ---
@staff_required
def booking_list(request):
    bookings = Booking.objects.all().order_by('-created_at')
    return render(request, 'staff_panel/orders/booking_list.html', {'bookings': bookings})

@staff_required
def booking_detail(request, pk):
    booking = get_object_or_404(Booking, pk=pk)
    if request.method == 'POST':
        form = BookingStatusForm(request.POST, instance=booking)
        if form.is_valid():
            form.save()
            messages.success(request, f"Booking #{booking.pk} status updated.")
            return redirect('staff_panel:booking_detail', pk=booking.pk)
    else:
        form = BookingStatusForm(instance=booking)
    return render(request, 'staff_panel/orders/booking_detail.html', {'booking': booking, 'form': form})

# --- PAYMENTS VIEWS ---
@staff_required
def payment_list(request):
    payments = Payment.objects.all().order_by('-created_at')
    return render(request, 'staff_panel/payments/payment_list.html', {'payments': payments})

@staff_required
def payment_verify(request, pk):
    payment = get_object_or_404(Payment, pk=pk)
    if request.method == 'POST':
        action = request.POST.get('action')
        if action == 'verify':
            payment.status = 'VERIFIED'
            payment.paid_at = timezone.now()
            payment.save()
            messages.success(request, f"Payment #{payment.pk} verified.")
        elif action == 'reject':
            payment.status = 'FAILED'
            payment.save()
            messages.warning(request, f"Payment #{payment.pk} rejected.")
        return redirect('staff_panel:payment_list')
    return render(request, 'staff_panel/payments/payment_verify.html', {'payment': payment})

# --- ACCOUNTS VIEWS ---
@staff_required
def user_list(request):
    users = User.objects.all().order_by('-date_joined')
    return render(request, 'staff_panel/accounts/user_list.html', {'users': users})

@staff_required
def user_detail(request, pk):
    user = get_object_or_404(User, pk=pk)
    return render(request, 'staff_panel/accounts/user_detail.html', {'user_obj': user})

@staff_required
def user_update(request, pk):
    user = get_object_or_404(User, pk=pk)
    if request.method == 'POST':
        form = UserAdminForm(request.POST, request.FILES, instance=user)
        if form.is_valid():
            form.save()
            messages.success(request, f"User '{user.username}' updated successfully.")
            return redirect('staff_panel:user_list')
    else:
        form = UserAdminForm(instance=user)
    return render(request, 'staff_panel/accounts/user_form.html', {'form': form, 'title': f'Edit User: {user.username}', 'user_obj': user})

@staff_required
def user_delete(request, pk):
    user = get_object_or_404(User, pk=pk)
    if request.method == 'POST':
        user.delete()
        messages.success(request, "User deleted successfully.")
        return redirect('staff_panel:user_list')
    return render(request, 'staff_panel/confirm_delete.html', {'object_name': f"User: {user.username}", 'cancel_url': 'staff_panel:user_list'})

