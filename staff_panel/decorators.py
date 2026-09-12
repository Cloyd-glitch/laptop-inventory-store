from functools import wraps
from django.shortcuts import redirect
from django.contrib import messages


def staff_required(view_func):
    """Require is_staff=True or ADMIN role."""
    @wraps(view_func)
    def _wrapped(request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect('/accounts/login/?next=' + request.path)
        if not (request.user.is_staff or request.user.is_superuser or request.user.is_admin_role):
            messages.error(request, "Staff access required.")
            return redirect('catalog:list')
        return view_func(request, *args, **kwargs)
    return _wrapped
