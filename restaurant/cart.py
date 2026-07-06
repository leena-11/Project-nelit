from decimal import Decimal
from django.conf import settings
from restaurant.models import MenuItem

class Cart:
    def __init__(self, request):
        self.session = request.session
        cart = self.session.get('cart')
        if not cart:
            cart = self.session['cart'] = {}
        self.cart = cart

    def add(self, menu_item, quantity=1, override_quantity=False):
        item_id = str(menu_item.id)
        if item_id not in self.cart:
            self.cart[item_id] = {
                'quantity': 0,
                'price': str(menu_item.price)
            }
        
        if override_quantity:
            self.cart[item_id]['quantity'] = quantity
        else:
            self.cart[item_id]['quantity'] += quantity
        
        # Check if quantity is 0 or less, remove it
        if self.cart[item_id]['quantity'] <= 0:
            self.remove(menu_item)
        else:
            self.save()

    def remove(self, menu_item):
        item_id = str(menu_item.id)
        if item_id in self.cart:
            del self.cart[item_id]
            self.save()

    def save(self):
        self.session.modified = True

    def __iter__(self):
        menu_item_ids = self.cart.keys()
        menu_items = MenuItem.objects.filter(id__in=menu_item_ids)
        menu_items_map = {str(item.id): item for item in menu_items}

        for item_id, item_data in self.cart.items():
            # Yield a fresh dict — do NOT mutate self.cart with non-serializable types
            price = Decimal(item_data['price'])
            quantity = item_data['quantity']
            yield {
                'menu_item': menu_items_map.get(item_id),
                'price': price,
                'quantity': quantity,
                'total_price': price * quantity,
            }

    def __len__(self):
        return sum(item['quantity'] for item in self.cart.values())

    def get_subtotal(self):
        return sum(Decimal(item['price']) * item['quantity'] for item in self.cart.values())

    def get_gst(self):
        return (self.get_subtotal() * Decimal('0.05')).quantize(Decimal('1.'))

    def get_total(self):
        return self.get_subtotal() + self.get_gst()

    def clear(self):
        del self.session['cart']
        self.save()
