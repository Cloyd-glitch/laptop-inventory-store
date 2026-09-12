from django.contrib import admin
from django.utils.html import format_html
from .models import Order, OrderItem, Booking


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0
    readonly_fields = ('laptop', 'quantity', 'unit_price', 'subtotal_display')
    can_delete = False

    def subtotal_display(self, obj):
        return f"₱{obj.subtotal:,.2f}"
    subtotal_display.short_description = "Subtotal"


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'customer', 'status', 'total_amount_display', 'created_at')
    list_filter = ('status', 'created_at')
    search_fields = ('customer__username', 'customer__email', 'id')
    readonly_fields = ('created_at', 'updated_at', 'total_amount')
    inlines = [OrderItemInline]
    ordering = ('-created_at',)

    def total_amount_display(self, obj):
        return format_html('<strong>₱{}</strong>', f"{obj.total_amount:,.2f}")
    total_amount_display.short_description = "Total"


@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = ('id', 'customer', 'laptop', 'status', 'expires_at', 'created_at')
    list_filter = ('status',)
    search_fields = ('customer__username', 'laptop__model_name', 'laptop__brand')
    readonly_fields = ('created_at', 'updated_at', 'expires_at')
    ordering = ('-created_at',)
