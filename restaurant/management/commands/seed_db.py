import os
import shutil
import urllib.request
from django.core.management.base import BaseCommand
from django.conf import settings
from restaurant.models import Category, MenuItem

class Command(BaseCommand):
    help = 'Seeds the database with categories and menu items'

    def handle(self, *args, **kwargs):
        self.stdout.write("Seeding database...")

        # Ensure directories exist
        categories_dir = os.path.join(settings.MEDIA_ROOT, 'categories')
        menu_dir = os.path.join(settings.MEDIA_ROOT, 'menu')
        os.makedirs(categories_dir, exist_ok=True)
        os.makedirs(menu_dir, exist_ok=True)

        # 1. Seed Categories
        categories_data = [
            {'name': 'Appetizers', 'slug': 'appetizers', 'image_name': 'appetizers.png'},
            {'name': 'Main Course', 'slug': 'main-course', 'image_name': 'main-course.png'},
            {'name': 'Desserts', 'slug': 'desserts', 'image_name': 'desserts.png'},
            {'name': 'Beverages', 'slug': 'beverages', 'image_name': 'beverages.png'},
        ]

        categories = {}
        for cat in categories_data:
            img_rel_path = f"categories/{cat['image_name']}"
            
            category, created = Category.objects.get_or_create(
                slug=cat['slug'],
                defaults={
                    'name': cat['name'],
                    'image': img_rel_path
                }
            )
            categories[cat['slug']] = category
            if created:
                self.stdout.write(f"Created category: {cat['name']}")
            else:
                self.stdout.write(f"Category already exists: {cat['name']}")

        # Fallback image path if downloads fail
        fallback_source = os.path.join(menu_dir, 'veg_spring_rolls.png')

        # 2. Seed Menu Items
        menu_items_data = [
            {
                'category_slug': 'appetizers',
                'name': 'Veg Spring Rolls',
                'description': 'Crispy golden rolls stuffed with seasoned vegetables. Served with sweet chili sauce.',
                'price': 120.00,
                'is_veg': True,
                'image_name': 'veg_spring_rolls.png',
                'url': None
            },
            {
                'category_slug': 'appetizers',
                'name': 'Chicken Wings',
                'description': 'Spicy and crispy buffalo chicken wings tossed in hot sauce.',
                'price': 180.00,
                'is_veg': False,
                'image_name': 'chicken_wings.png',
                'url': 'https://images.unsplash.com/photo-1567620832903-9fc6debc209f?w=500&auto=format&fit=crop&q=80'
            },
            {
                'category_slug': 'main-course',
                'name': 'Margherita Pizza',
                'description': 'Classic Italian pizza with fresh tomato sauce, mozzarella cheese, and basil leaves.',
                'price': 250.00,
                'is_veg': True,
                'image_name': 'margherita_pizza.png',
                'url': 'https://images.unsplash.com/photo-1604382354936-07c5d9983bd3?w=500&auto=format&fit=crop&q=80'
            },
            {
                'category_slug': 'main-course',
                'name': 'Paneer Butter Masala',
                'description': 'Rich and creamy curry made with cottage cheese cubes in a spiced tomato-butter gravy.',
                'price': 220.00,
                'is_veg': True,
                'image_name': 'paneer_butter_masala.png',
                'url': 'https://images.unsplash.com/photo-1631452180519-c014fe946bc7?w=500&auto=format&fit=crop&q=80'
            },
            {
                'category_slug': 'desserts',
                'name': 'Chocolate Brownie',
                'description': 'Warm fudgy chocolate brownie served with chocolate drizzle.',
                'price': 140.00,
                'is_veg': True,
                'image_name': 'chocolate_brownie.png',
                'url': 'https://images.unsplash.com/photo-1606313564200-e75d5e30476c?w=500&auto=format&fit=crop&q=80'
            },
            {
                'category_slug': 'desserts',
                'name': 'Gulab Jamun',
                'description': 'Soft, golden-brown fried milk dumplings soaked in aromatic cardamom sugar syrup.',
                'price': 90.00,
                'is_veg': True,
                'image_name': 'gulab_jamun.png',
                'url': 'https://images.unsplash.com/photo-1585032226651-759b368d7246?w=500&auto=format&fit=crop&q=80'
            },
            {
                'category_slug': 'beverages',
                'name': 'Cold Coffee',
                'description': 'Chilled milk blended with premium coffee, topped with vanilla ice cream.',
                'price': 110.00,
                'is_veg': True,
                'image_name': 'cold_coffee.png',
                'url': 'https://images.unsplash.com/photo-1517701604599-bb29b565090c?w=500&auto=format&fit=crop&q=80'
            },
            {
                'category_slug': 'beverages',
                'name': 'Fresh Lime Soda',
                'description': 'Tangy lime juice mixed with sparkling soda, served sweet or salted.',
                'price': 80.00,
                'is_veg': True,
                'image_name': 'fresh_lime_soda.png',
                'url': 'https://images.unsplash.com/photo-1513558161293-cdaf765ed2fd?w=500&auto=format&fit=crop&q=80'
            },
            {
                'category_slug': 'appetizers',
                'name': 'Punjabi Samosa',
                'description': 'Crispy pastry filled with spiced potatoes and peas, served with mint chutney.',
                'price': 50.00,
                'is_veg': True,
                'image_name': 'samosa.png',
                'url': 'https://images.unsplash.com/photo-1601050690597-df0568f70950?w=500&auto=format&fit=crop&q=80'
            },
            {
                'category_slug': 'appetizers',
                'name': 'Paneer Tikka',
                'description': 'Cottage cheese cubes marinated in yogurt and spices, grilled in a tandoor.',
                'price': 160.00,
                'is_veg': True,
                'image_name': 'paneer_tikka.png',
                'url': 'https://images.unsplash.com/photo-1599487405270-81710b37bc99?w=500&auto=format&fit=crop&q=80'
            },
            {
                'category_slug': 'appetizers',
                'name': 'French Fries',
                'description': 'Crispy golden potato fries lightly salted.',
                'price': 90.00,
                'is_veg': True,
                'image_name': 'french_fries.png',
                'url': 'https://images.unsplash.com/photo-1576107232684-1279f3908594?w=500&auto=format&fit=crop&q=80'
            },
            {
                'category_slug': 'main-course',
                'name': 'Butter Chicken',
                'description': 'Tender chicken pieces cooked in a rich, creamy tomato and butter sauce.',
                'price': 280.00,
                'is_veg': False,
                'image_name': 'butter_chicken.png',
                'url': 'https://images.unsplash.com/photo-1603894584373-5ac82b2ae398?w=500&auto=format&fit=crop&q=80'
            },
            {
                'category_slug': 'main-course',
                'name': 'Dal Makhani',
                'description': 'Slow-cooked black lentils and kidney beans with butter and cream.',
                'price': 180.00,
                'is_veg': True,
                'image_name': 'dal_makhani.png',
                'url': 'https://images.unsplash.com/photo-1546833999-b9f581a1996d?w=500&auto=format&fit=crop&q=80'
            },
            {
                'category_slug': 'main-course',
                'name': 'Veg Biryani',
                'description': 'Fragrant basmati rice cooked with mixed vegetables and aromatic spices.',
                'price': 200.00,
                'is_veg': True,
                'image_name': 'veg_biryani.png',
                'url': 'https://images.unsplash.com/photo-1563379091339-03b21ab4a4f8?w=500&auto=format&fit=crop&q=80'
            },
            {
                'category_slug': 'main-course',
                'name': 'Garlic Naan',
                'description': 'Soft Indian flatbread topped with minced garlic and cilantro, baked in tandoor.',
                'price': 40.00,
                'is_veg': True,
                'image_name': 'garlic_naan.png',
                'url': 'https://images.unsplash.com/photo-1626074353765-517a681e40be?w=500&auto=format&fit=crop&q=80'
            },
            {
                'category_slug': 'desserts',
                'name': 'Rasmalai',
                'description': 'Soft cheese patties immersed in chilled, creamy, saffron-flavored milk.',
                'price': 110.00,
                'is_veg': True,
                'image_name': 'rasmalai.png',
                'url': 'https://images.unsplash.com/photo-1579372786545-d24232daf58c?w=500&auto=format&fit=crop&q=80'
            },
            {
                'category_slug': 'desserts',
                'name': 'Vanilla Ice Cream',
                'description': 'Classic creamy vanilla ice cream scoops.',
                'price': 70.00,
                'is_veg': True,
                'image_name': 'vanilla_ice_cream.png',
                'url': 'https://images.unsplash.com/photo-1570197571499-166b36435e9f?w=500&auto=format&fit=crop&q=80'
            },
            {
                'category_slug': 'desserts',
                'name': 'Gajar Ka Halwa',
                'description': 'Warm, sweet carrot pudding cooked with milk, ghee, and nuts.',
                'price': 120.00,
                'is_veg': True,
                'image_name': 'gajar_halwa.png',
                'url': 'https://t3.ftcdn.net/jpg/02/76/86/35/360_F_276863544_V3l86xK5qZkC2NfM54D592C4W2595B0J.jpg'
            },
            {
                'category_slug': 'beverages',
                'name': 'Mango Lassi',
                'description': 'Sweet and creamy yogurt-based drink blended with fresh mango pulp.',
                'price': 80.00,
                'is_veg': True,
                'image_name': 'mango_lassi.png',
                'url': 'https://images.unsplash.com/photo-1544145945-f90425340c7e?w=500&auto=format&fit=crop&q=80'
            },
            {
                'category_slug': 'beverages',
                'name': 'Masala Chai',
                'description': 'Traditional Indian tea brewed with milk and aromatic spices.',
                'price': 30.00,
                'is_veg': True,
                'image_name': 'masala_chai.png',
                'url': 'https://images.unsplash.com/photo-1561336313-0bd5e0b27ec8?w=500&auto=format&fit=crop&q=80'
            },
        ]

        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'}

        for item_data in menu_items_data:
            img_rel_path = f"menu/{item_data['image_name']}"
            img_abs_path = os.path.join(settings.MEDIA_ROOT, img_rel_path)

            if not os.path.exists(img_abs_path) and item_data['url']:
                try:
                    self.stdout.write(f"Downloading image for {item_data['name']}...")
                    req = urllib.request.Request(item_data['url'], headers=headers)
                    with urllib.request.urlopen(req, timeout=10) as response, open(img_abs_path, 'wb') as out_file:
                        shutil.copyfileobj(response, out_file)
                    self.stdout.write(f"Downloaded image successfully.")
                except Exception as e:
                    self.stdout.write(self.style.WARNING(f"Failed to download image for {item_data['name']}: {e}. Copying fallback image."))
                    if os.path.exists(fallback_source):
                        shutil.copy(fallback_source, img_abs_path)
                    else:
                        try:
                            from PIL import Image, ImageDraw
                            img = Image.new('RGB', (300, 200), color=(255, 140, 0))
                            d = ImageDraw.Draw(img)
                            d.text((10,10), item_data['name'], fill=(255,255,255))
                            img.save(img_abs_path)
                        except Exception as pe:
                            self.stdout.write(self.style.ERROR(f"Could not create dummy image: {pe}"))

            item, created = MenuItem.objects.get_or_create(
                name=item_data['name'],
                defaults={
                    'category': categories[item_data['category_slug']],
                    'description': item_data['description'],
                    'price': item_data['price'],
                    'is_veg': item_data['is_veg'],
                    'image': img_rel_path
                }
            )
            if created:
                self.stdout.write(f"Created menu item: {item_data['name']}")
            else:
                item.image = img_rel_path
                item.price = item_data['price']
                item.is_veg = item_data['is_veg']
                item.save()
                self.stdout.write(f"Menu item already exists: {item_data['name']}")

        self.stdout.write(self.style.SUCCESS("Database seeding completed!"))
