from django.core.management.base import BaseCommand
from store.models import Category, Product


class Command(BaseCommand):
    help = 'Seeds the database with sample categories and products'

    def handle(self, *args, **options):
        # Categories
        categories_data = [
            {'name': 'Phones', 'slug': 'phones'},
            {'name': 'Laptops', 'slug': 'laptops'},
            {'name': 'PC Components', 'slug': 'pc-components'},
            {'name': 'Monitors', 'slug': 'monitors'},
            {'name': 'Accessories', 'slug': 'accessories'},
            {'name': 'Gaming Gear', 'slug': 'gaming-gear'},
        ]

        created_categories = {}
        for cat_data in categories_data:
            cat, created = Category.objects.get_or_create(
                slug=cat_data['slug'],
                defaults={'name': cat_data['name']}
            )
            created_categories[cat_data['name']] = cat
            status = 'Created' if created else 'Already exists'
            self.stdout.write(f"  {status}: {cat.name}")

        # Products
        products_data = [
            {
                'name': 'iPhone 15 Pro',
                'category': 'Phones',
                'description': 'Apple iPhone 15 Pro with A17 Pro chip, titanium design, and advanced camera system. Features a 6.1-inch Super Retina XDR display with ProMotion technology.',
                'price': 999.99,
                'stock': 25,
            },
            {
                'name': 'Samsung Galaxy S24 Ultra',
                'category': 'Phones',
                'description': 'Samsung Galaxy S24 Ultra with Snapdragon 8 Gen 3, built-in S Pen, and AI-powered features. 6.8-inch Dynamic AMOLED display with 120Hz refresh rate.',
                'price': 1199.99,
                'stock': 20,
            },
            {
                'name': 'Google Pixel 8 Pro',
                'category': 'Phones',
                'description': 'Google Pixel 8 Pro with Tensor G3 chip, advanced AI photography, and 7 years of OS updates. 6.7-inch Super Actua display.',
                'price': 899.99,
                'stock': 15,
            },
            {
                'name': 'Dell XPS 15',
                'category': 'Laptops',
                'description': 'Dell XPS 15 with Intel Core i7, 16GB RAM, 512GB SSD, and NVIDIA GeForce RTX 4050. Stunning 15.6-inch OLED 3.5K display.',
                'price': 1499.99,
                'stock': 10,
            },
            {
                'name': 'ASUS ROG Strix G16',
                'category': 'Laptops',
                'description': 'ASUS ROG Strix G16 gaming laptop with Intel Core i9, 32GB RAM, 1TB SSD, and NVIDIA RTX 4070. 16-inch QHD 240Hz display.',
                'price': 1899.99,
                'stock': 8,
            },
            {
                'name': 'MacBook Air M3',
                'category': 'Laptops',
                'description': 'Apple MacBook Air with M3 chip, 8GB unified memory, 256GB SSD. Ultra-thin design with 13.6-inch Liquid Retina display and 18-hour battery life.',
                'price': 1099.99,
                'stock': 18,
            },
            {
                'name': 'NVIDIA RTX 4070 Super',
                'category': 'PC Components',
                'description': 'NVIDIA GeForce RTX 4070 Super graphics card with 12GB GDDR6X memory. Excellent for 1440p gaming and content creation with DLSS 3 support.',
                'price': 599.99,
                'stock': 12,
            },
            {
                'name': 'AMD Ryzen 7 7800X3D',
                'category': 'PC Components',
                'description': 'AMD Ryzen 7 7800X3D processor with 3D V-Cache technology. 8 cores, 16 threads, up to 5.0GHz boost. The ultimate gaming CPU.',
                'price': 349.99,
                'stock': 20,
            },
            {
                'name': 'Corsair Vengeance DDR5 32GB',
                'category': 'PC Components',
                'description': 'Corsair Vengeance DDR5 32GB (2x16GB) RAM kit, 5600MHz speed. Optimized for Intel and AMD platforms with XMP 3.0 support.',
                'price': 89.99,
                'stock': 30,
            },
            {
                'name': 'LG UltraGear 27" 4K',
                'category': 'Monitors',
                'description': 'LG UltraGear 27-inch 4K UHD gaming monitor with 144Hz refresh rate, 1ms response time, and NVIDIA G-Sync compatibility. IPS panel with HDR600.',
                'price': 449.99,
                'stock': 14,
            },
            {
                'name': 'Samsung Odyssey G9 49"',
                'category': 'Monitors',
                'description': 'Samsung Odyssey G9 49-inch ultrawide curved gaming monitor. Dual QHD (5120x1440), 240Hz, 1ms, with Quantum Mini-LED technology.',
                'price': 1299.99,
                'stock': 5,
            },
            {
                'name': 'Logitech MX Master 3S',
                'category': 'Accessories',
                'description': 'Logitech MX Master 3S wireless mouse with MagSpeed scroll wheel, 8K DPI sensor, and quiet clicks. Multi-device connectivity via Bluetooth.',
                'price': 99.99,
                'stock': 40,
            },
            {
                'name': 'Apple AirPods Pro 2',
                'category': 'Accessories',
                'description': 'Apple AirPods Pro 2nd generation with H2 chip, adaptive transparency, and personalized spatial audio. USB-C charging case.',
                'price': 249.99,
                'stock': 35,
            },
            {
                'name': 'Razer DeathAdder V3 Pro',
                'category': 'Gaming Gear',
                'description': 'Razer DeathAdder V3 Pro wireless gaming mouse with Focus Pro 30K optical sensor. Ultra-lightweight at 63g with up to 90-hour battery life.',
                'price': 149.99,
                'stock': 22,
            },
            {
                'name': 'SteelSeries Apex Pro TKL',
                'category': 'Gaming Gear',
                'description': 'SteelSeries Apex Pro TKL mechanical gaming keyboard with adjustable OmniPoint switches. OLED smart display and aircraft-grade aluminum frame.',
                'price': 189.99,
                'stock': 16,
            },
            {
                'name': 'HyperX Cloud III Wireless',
                'category': 'Gaming Gear',
                'description': 'HyperX Cloud III Wireless gaming headset with 53mm drivers, DTS Spatial Audio, and 120-hour battery life. Memory foam ear cushions.',
                'price': 169.99,
                'stock': 18,
            },
        ]

        for prod_data in products_data:
            category = created_categories.get(prod_data['category'])
            if category:
                product, created = Product.objects.get_or_create(
                    name=prod_data['name'],
                    defaults={
                        'category': category,
                        'description': prod_data['description'],
                        'price': prod_data['price'],
                        'stock': prod_data['stock'],
                        'is_available': True,
                    }
                )
                status = 'Created' if created else 'Already exists'
                self.stdout.write(f"  {status}: {product.name}")

        self.stdout.write(self.style.SUCCESS('\nSeed data loaded successfully!'))
