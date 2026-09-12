from django.contrib import admin
from django.utils.html import format_html
from .models import Category, Laptop, LaptopImage


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug', 'laptop_count')
    prepopulated_fields = {'slug': ('name',)}
    search_fields = ('name',)

    def laptop_count(self, obj):
        return obj.laptops.count()
    laptop_count.short_description = "Laptops"


class LaptopImageInline(admin.TabularInline):
    model = LaptopImage
    extra = 2
    fields = ('image', 'caption', 'thumb_preview')
    readonly_fields = ('thumb_preview',)

    def thumb_preview(self, obj):
        if obj.image:
            return format_html('<img src="{}" style="height:50px;border-radius:4px;" />', obj.image.url)
        return "—"
    thumb_preview.short_description = "Preview"


@admin.register(Laptop)
class LaptopAdmin(admin.ModelAdmin):
    list_display = (
        'image_preview', 'brand', 'model_name', 'category',
        'price', 'stock_quantity', 'condition', 'is_active'
    )
    list_display_links = ('image_preview', 'brand', 'model_name')
    list_filter = ('brand', 'category', 'condition', 'is_active')
    search_fields = ('brand', 'model_name', 'processor', 'description')
    prepopulated_fields = {'slug': ('brand', 'model_name')}
    list_editable = ('price', 'stock_quantity', 'is_active')
    list_per_page = 25
    inlines = [LaptopImageInline]
    fieldsets = (
        ('Identity', {
            'fields': ('brand', 'model_name', 'slug', 'category', 'condition', 'is_active')
        }),
        ('Specifications', {
            'fields': ('processor', 'ram', 'storage', 'gpu', 'screen_size', 'operating_system')
        }),
        ('Pricing & Stock', {
            'fields': ('price', 'stock_quantity')
        }),
        ('Media & Description', {
            'fields': ('main_image', 'description')
        }),
    )
    actions = ['mark_active', 'mark_inactive']

    def image_preview(self, obj):
        if obj.main_image:
            return format_html('<img src="{}" style="height:48px;border-radius:6px;box-shadow:0 2px 6px rgba(0,0,0,.4);" />', obj.main_image.url)
        return format_html('<span style="color:#888;">—</span>')
    image_preview.short_description = "Photo"

    @admin.action(description="✓ Mark selected as Active")
    def mark_active(self, request, queryset):
        queryset.update(is_active=True)

    @admin.action(description="✗ Mark selected as Inactive")
    def mark_inactive(self, request, queryset):
        queryset.update(is_active=False)