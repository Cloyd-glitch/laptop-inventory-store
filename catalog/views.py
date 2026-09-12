from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator
from django.db.models import Q
from .models import Laptop, Category


def catalog_list_view(request):
    laptops = Laptop.objects.filter(is_active=True).select_related('category')

    # --- Filters ---
    query = request.GET.get('q', '').strip()
    category_slug = request.GET.get('category', '')
    brand = request.GET.get('brand', '')
    condition = request.GET.get('condition', '')
    min_price = request.GET.get('min_price', '')
    max_price = request.GET.get('max_price', '')
    sort = request.GET.get('sort', '-created_at')

    if query:
        laptops = laptops.filter(
            Q(brand__icontains=query) |
            Q(model_name__icontains=query) |
            Q(processor__icontains=query) |
            Q(description__icontains=query)
        )
    if category_slug:
        laptops = laptops.filter(category__slug=category_slug)
    if brand:
        laptops = laptops.filter(brand__iexact=brand)
    if condition:
        laptops = laptops.filter(condition=condition)
    if min_price:
        try:
            laptops = laptops.filter(price__gte=float(min_price))
        except ValueError:
            pass
    if max_price:
        try:
            laptops = laptops.filter(price__lte=float(max_price))
        except ValueError:
            pass

    SORT_OPTIONS = {
        'price_asc': 'price',
        'price_desc': '-price',
        'newest': '-created_at',
        'name_asc': 'model_name',
    }
    laptops = laptops.order_by(SORT_OPTIONS.get(sort, '-created_at'))

    paginator = Paginator(laptops, 12)
    page_obj = paginator.get_page(request.GET.get('page'))

    categories = Category.objects.all()
    brands = Laptop.objects.filter(is_active=True).values_list('brand', flat=True).distinct().order_by('brand')
    conditions = Laptop.Condition.choices

    context = {
        'page_obj': page_obj,
        'categories': categories,
        'brands': brands,
        'conditions': conditions,
        'query': query,
        'selected_category': category_slug,
        'selected_brand': brand,
        'selected_condition': condition,
        'min_price': min_price,
        'max_price': max_price,
        'sort': sort,
        'total_count': laptops.count(),
    }
    return render(request, 'catalog/list.html', context)


def laptop_detail_view(request, slug):
    laptop = get_object_or_404(Laptop, slug=slug, is_active=True)
    gallery = laptop.gallery_images.all()
    related = Laptop.objects.filter(
        category=laptop.category, is_active=True
    ).exclude(pk=laptop.pk)[:4]

    context = {
        'laptop': laptop,
        'gallery': gallery,
        'related': related,
    }
    return render(request, 'catalog/detail.html', context)
