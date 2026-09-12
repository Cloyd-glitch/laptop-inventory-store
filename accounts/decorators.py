from functools import wraps
from django.shortcuts import redirect
from django.contrib import messages


def customer_required(view_func):
    """Allow only authenticated users with CUSTOMER role."""
    @wraps(view_func)
    def _wrapped(request, *args, **kwargs):
        if not request.user.is_authenticated:
            messages.warning(request, "Please log in to continue.")
            return redirect('accounts:login')
        if not request.user.is_customer:
            messages.error(request, "Access restricted to customers.")
            return redirect('catalog:list')
        return view_func(request, *args, **kwargs)
    return _wrapped


def admin_required(view_func):
    """Allow only authenticated admin-role users."""
    @wraps(view_func)
    def _wrapped(request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect('accounts:login')
        if not request.user.is_admin_role:
            messages.error(request, "Admin access required.")
            return redirect('catalog:list')
        return view_func(request, *args, **kwargs)
    return _wrapped
