from decimal import Decimal
from catalog.models import Laptop


CART_SESSION_KEY = 'cart'


class Cart:
    """Session-backed shopping cart."""

    def __init__(self, request):
        self.session = request.session
        cart = self.session.get(CART_SESSION_KEY)
        if cart is None:
            cart = self.session[CART_SESSION_KEY] = {}
        self.cart = cart

    # ------------------------------------------------------------------
    def add(self, laptop, quantity=1, override_quantity=False):
        key = str(laptop.pk)
        if key not in self.cart:
            self.cart[key] = {
                'laptop_id': laptop.pk,
                'quantity': 0,
                'price': str(laptop.price),
                'brand': laptop.brand,
                'model_name': laptop.model_name,
                'slug': laptop.slug,
                'main_image': laptop.main_image.url if laptop.main_image else '',
            }
        if override_quantity:
            self.cart[key]['quantity'] = quantity
        else:
            self.cart[key]['quantity'] += quantity
        self._save()

    def remove(self, laptop_id):
        key = str(laptop_id)
        if key in self.cart:
            del self.cart[key]
            self._save()

    def update(self, laptop_id, quantity):
        key = str(laptop_id)
        if key in self.cart:
            if quantity <= 0:
                self.remove(laptop_id)
            else:
                self.cart[key]['quantity'] = quantity
                self._save()

    def clear(self):
        self.session[CART_SESSION_KEY] = {}
        self.cart = self.session[CART_SESSION_KEY]
        self._save()

    def _save(self):
        self.session.modified = True

    # ------------------------------------------------------------------
    def __iter__(self):
        """Yield enriched item dicts with subtotal Decimal."""
        laptop_ids = [item['laptop_id'] for item in self.cart.values()]
        laptops = {lp.pk: lp for lp in Laptop.objects.filter(pk__in=laptop_ids)}
        for item in self.cart.values():
            item = item.copy()
            item['price'] = Decimal(item['price'])
            item['subtotal'] = item['price'] * item['quantity']
            item['laptop'] = laptops.get(item['laptop_id'])
            yield item

    def __len__(self):
        return sum(item['quantity'] for item in self.cart.values())

    @property
    def total_price(self):
        return sum(Decimal(item['price']) * item['quantity'] for item in self.cart.values())

    @property
    def items_raw(self):
        return self.cart
