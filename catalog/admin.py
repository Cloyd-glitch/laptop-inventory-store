from django.contrib import admin
from django.utils.html import format_html
from .models import Category, Laptop, LaptopImage


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug')
    prepopulated_fields = {'slug': ('name',)}


class LaptopImageInline(admin.TabularInline):
    model = LaptopImage
    extra = 1


@admin.register(Laptop)
class LaptopAdmin(admin.ModelAdmin):
    list_display = ('brand', 'model_name', 'category', 'price', 'stock_quantity', 'condition', 'is_active', 'image_preview')
    list_filter = ('brand', 'category', 'condition', 'is_active')
    search_fields = ('brand', 'model_name', 'processor')
    prepopulated_fields = {'slug': ('brand', 'model_name')}
    inlines = [LaptopImageInline]

    def image_preview(self, obj):
        if obj.main_image:
            return format_html('<img src="{}" style="height:50px; border-radius:4px;" />', obj.main_image.url)
        return "—"
    image_preview.short_description = "Preview"