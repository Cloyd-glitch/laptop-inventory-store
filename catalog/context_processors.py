from orders.cart import Cart


def cart_item_count(request):
    """Inject cart item count into every template context."""
    cart = Cart(request)
    return {'cart_item_count': len(cart)}
