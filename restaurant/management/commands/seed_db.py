from django.core.management.base import BaseCommand
from restaurant.models import Category, MenuItem


class Command(BaseCommand):
    help = 'Seeds the database with categories and menu items (images served from static files)'

    def handle(self, *args, **kwargs):
        self.stdout.write("Seeding database...")

        # 1. Seed Categories
        # Image paths reference static/images/categories/ (served via collectstatic)
        categories_data = [
            {'name': 'Appetizers', 'slug': 'appetizers', 'image_name': 'categories/appetizers.png'},
            {'name': 'Main Course', 'slug': 'main-course', 'image_name': 'categories/main-course.png'},
            {'name': 'Desserts', 'slug': 'desserts', 'image_name': 'categories/desserts.png'},
            {'name': 'Beverages', 'slug': 'beverages', 'image_name': 'categories/beverages.png'},
        ]

        categories = {}
        for cat in categories_data:
            category, created = Category.objects.get_or_create(
                slug=cat['slug'],
                defaults={
                    'name': cat['name'],
                    'image': cat['image_name']
                }
            )
            if not created:
                # Update image path to match static files layout
                category.image = cat['image_name']
                category.save()
            categories[cat['slug']] = category
            action = "Created" if created else "Updated"
            self.stdout.write(f"{action} category: {cat['name']}")

        # 2. Seed Menu Items
        # Image paths reference static/images/menu/ (served via collectstatic)
        menu_items_data = [
            {
                'category_slug': 'appetizers',
                'name': 'Veg Spring Rolls',
                'description': 'Crispy golden rolls stuffed with seasoned vegetables. Served with sweet chili sauce.',
                'price': 120.00,
                'is_veg': True,
                'image_name': 'menu/veg_spring_rolls.png',
            },
            {
                'category_slug': 'appetizers',
                'name': 'Chicken Wings',
                'description': 'Spicy and crispy buffalo chicken wings tossed in hot sauce.',
                'price': 180.00,
                'is_veg': False,
                'image_name': 'menu/chicken_wings.png',
            },
            {
                'category_slug': 'main-course',
                'name': 'Margherita Pizza',
                'description': 'Classic Italian pizza with fresh tomato sauce, mozzarella cheese, and basil leaves.',
                'price': 250.00,
                'is_veg': True,
                'image_name': 'menu/margherita_pizza.png',
            },
            {
                'category_slug': 'main-course',
                'name': 'Paneer Butter Masala',
                'description': 'Rich and creamy curry made with cottage cheese cubes in a spiced tomato-butter gravy.',
                'price': 220.00,
                'is_veg': True,
                'image_name': 'menu/paneer_butter_masala.png',
            },
            {
                'category_slug': 'desserts',
                'name': 'Chocolate Brownie',
                'description': 'Warm fudgy chocolate brownie served with chocolate drizzle.',
                'price': 140.00,
                'is_veg': True,
                'image_name': 'menu/chocolate_brownie.png',
            },
            {
                'category_slug': 'desserts',
                'name': 'Gulab Jamun',
                'description': 'Soft, golden-brown fried milk dumplings soaked in aromatic cardamom sugar syrup.',
                'price': 90.00,
                'is_veg': True,
                'image_name': 'menu/gulab_jamun.png',
            },
            {
                'category_slug': 'beverages',
                'name': 'Cold Coffee',
                'description': 'Chilled milk blended with premium coffee, topped with vanilla ice cream.',
                'price': 110.00,
                'is_veg': True,
                'image_name': 'menu/cold_coffee.png',
            },
            {
                'category_slug': 'beverages',
                'name': 'Fresh Lime Soda',
                'description': 'Tangy lime juice mixed with sparkling soda, served sweet or salted.',
                'price': 80.00,
                'is_veg': True,
                'image_name': 'menu/fresh_lime_soda.png',
            },
            {
                'category_slug': 'appetizers',
                'name': 'Punjabi Samosa',
                'description': 'Crispy pastry filled with spiced potatoes and peas, served with mint chutney.',
                'price': 50.00,
                'is_veg': True,
                'image_name': 'menu/samosa.png',
            },
            {
                'category_slug': 'appetizers',
                'name': 'Paneer Tikka',
                'description': 'Cottage cheese cubes marinated in yogurt and spices, grilled in a tandoor.',
                'price': 160.00,
                'is_veg': True,
                'image_name': 'menu/paneer_tikka.png',
            },
            {
                'category_slug': 'appetizers',
                'name': 'French Fries',
                'description': 'Crispy golden potato fries lightly salted.',
                'price': 90.00,
                'is_veg': True,
                'image_name': 'menu/french_fries.png',
            },
            {
                'category_slug': 'main-course',
                'name': 'Butter Chicken',
                'description': 'Tender chicken pieces cooked in a rich, creamy tomato and butter sauce.',
                'price': 280.00,
                'is_veg': False,
                'image_name': 'menu/butter_chicken.png',
            },
            {
                'category_slug': 'main-course',
                'name': 'Dal Makhani',
                'description': 'Slow-cooked black lentils and kidney beans with butter and cream.',
                'price': 180.00,
                'is_veg': True,
                'image_name': 'menu/dal_makhani.png',
            },
            {
                'category_slug': 'main-course',
                'name': 'Veg Biryani',
                'description': 'Fragrant basmati rice cooked with mixed vegetables and aromatic spices.',
                'price': 200.00,
                'is_veg': True,
                'image_name': 'menu/veg_biryani.png',
            },
            {
                'category_slug': 'main-course',
                'name': 'Garlic Naan',
                'description': 'Soft Indian flatbread topped with minced garlic and cilantro, baked in tandoor.',
                'price': 40.00,
                'is_veg': True,
                'image_name': 'menu/garlic_naan.png',
            },
            {
                'category_slug': 'desserts',
                'name': 'Rasmalai',
                'description': 'Soft cheese patties immersed in chilled, creamy, saffron-flavored milk.',
                'price': 110.00,
                'is_veg': True,
                'image_name': 'menu/rasmalai.png',
            },
            {
                'category_slug': 'desserts',
                'name': 'Vanilla Ice Cream',
                'description': 'Classic creamy vanilla ice cream scoops.',
                'price': 70.00,
                'is_veg': True,
                'image_name': 'menu/vanilla_ice_cream.png',
            },
            {
                'category_slug': 'desserts',
                'name': 'Gajar Ka Halwa',
                'description': 'Warm, sweet carrot pudding cooked with milk, ghee, and nuts.',
                'price': 120.00,
                'is_veg': True,
                'image_name': 'menu/gajar_halwa.png',
            },
            {
                'category_slug': 'beverages',
                'name': 'Mango Lassi',
                'description': 'Sweet and creamy yogurt-based drink blended with fresh mango pulp.',
                'price': 80.00,
                'is_veg': True,
                'image_name': 'menu/mango_lassi.png',
            },
            {
                'category_slug': 'beverages',
                'name': 'Masala Chai',
                'description': 'Traditional Indian tea brewed with milk and aromatic spices.',
                'price': 30.00,
                'is_veg': True,
                'image_name': 'menu/masala_chai.png',
            },
        ]

        for item_data in menu_items_data:
            item, created = MenuItem.objects.get_or_create(
                name=item_data['name'],
                defaults={
                    'category': categories[item_data['category_slug']],
                    'description': item_data['description'],
                    'price': item_data['price'],
                    'is_veg': item_data['is_veg'],
                    'image': item_data['image_name']
                }
            )
            if not created:
                # Update image path and other fields
                item.image = item_data['image_name']
                item.price = item_data['price']
                item.is_veg = item_data['is_veg']
                item.save()
            action = "Created" if created else "Updated"
            self.stdout.write(f"{action} menu item: {item_data['name']}")

        self.stdout.write(self.style.SUCCESS("Database seeding completed!"))
