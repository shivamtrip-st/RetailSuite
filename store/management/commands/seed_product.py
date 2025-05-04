import os
import requests
import tempfile
from django.core.management.base import BaseCommand
from django.core.files import File
from django.utils.text import slugify
from PIL import Image
from io import BytesIO

from store.models import Category, Product

class Command(BaseCommand):
    help = 'Seeds the database with product data'

    def handle(self, *args, **kwargs):
        self.stdout.write(self.style.SUCCESS('Starting database seeding...'))
        
        def download_image(url):
            response = requests.get(url)
            if response.status_code == 200:
                img = Image.open(BytesIO(response.content))
                
                if img.mode == 'RGBA':
                    img = img.convert('RGB')
                
                temp_file = tempfile.NamedTemporaryFile(delete=False, suffix='.jpg')
                img.save(temp_file.name, format='JPEG')
                
                return temp_file
            return None

        products_data = [
    # Electronics Category
    {
        'category_name': 'Electronics',
        'products': [
             {
                        'name': 'MorningStar Digital Clock',
                        'price': 29.99,
                        'description': 'Modern alarm clock with temperature display, USB charging port, and multiple alarm settings. Sleek design fits any bedroom decor.',
                        'image_url': 'https://images.unsplash.com/photo-1563861826100-9cb868fdbe1c',
                        'stock_quantity': 30,
                        'is_sale': True,
                        'sale_price': 24.99,
                    },
        ]
    },
    # Home & Kitchen Category
    {
        'category_name': 'Home & Kitchen',
        'products': [
            {
                        'name': 'GreenChef Cutting Boards',
                        'price': 32.99,
                        'description': 'Set of 3 eco-friendly bamboo cutting boards in different sizes. Water-resistant, knife-friendly, and sustainably sourced.',
                        'image_url': 'https://images.unsplash.com/photo-1594223274512-ad4803739b7c',
                        'stock_quantity': 25,
                        'is_sale': False,
                        'sale_price': 0.00,
                    },
        ]
    },
    # Office Supplies Category
    {
        'category_name': 'Office Supplies',
        'products': [
            {
                'name': 'OrganizePlus Desk Tray',
                'price': 24.99,
                'description': '3-tier metal desk organizer tray with a modern mesh design. Keeps your workspace tidy.',
                'image_url': 'https://images.unsplash.com/photo-1581291518838-0c5b5f4b2d9a',
                'stock_quantity': 30,
                'is_sale': False,
                'sale_price': 0.00,
            },
            {
                'name': 'NoteMaster Sticky Notes Set',
                'price': 12.99,
                'description': 'Color-coded sticky note pack with tabs and flags. Comes in a hard case for easy storage.',
                'image_url': 'https://images.unsplash.com/photo-1502920917128-1aa500764b6e',
                'stock_quantity': 50,
                'is_sale': True,
                'sale_price': 10.99,
            },
        ]
    },
    # Accessories Category
    {
        'category_name': 'Accessories',
        'products': [
            {
                        'name': 'ClassicWrite Notebook',
                        'price': 19.99,
                        'description': 'Premium faux leather journal with 240 lined pages of recycled paper. Elastic closure and built-in bookmark.',
                        'image_url': 'https://images.unsplash.com/photo-1531346878377-a5be20888e57',
                        'stock_quantity': 50,
                        'is_sale': False,
                        'sale_price': 0.00,
                    },
        ]
    },
    # Home Decor Category
    {
        'category_name': 'Home Decor',
        'products': [
          {
                        'name': 'CozyHome Pillow Covers',
                        'price': 19.99,
                        'description': 'Set of 2 decorative covers for 18x18 inch pillows. Soft fabric with hidden zipper. Machine washable.',
                        'image_url': 'https://images.unsplash.com/photo-1567225557594-88d73e55f2cb',
                        'stock_quantity': 40,
                        'is_sale': True,
                        'sale_price': 16.99,
                    },
        ]
    },
    # Tech Accessories Category
    {
   'category_name': 'Accessories',
                'products': [
                    {
                        'name': 'SlimFit RFID Wallet',
                        'price': 29.99,
                        'description': 'Ultra-thin card holder that blocks RFID signals. Holds up to 8 cards and includes a money clip. Perfect front pocket wallet.',
                        'image_url': 'https://images.unsplash.com/photo-1627123424574-724758594e93',
                        'stock_quantity': 30,
                        'is_sale': False,
                        'sale_price': 0.00,
                    },
                ]
    },
]

        
        for category_data in products_data:
            category_name = category_data['category_name']
            category, created = Category.objects.get_or_create(name=category_name)
            
            if created:
                self.stdout.write(self.style.SUCCESS(f"Created category: {category_name}"))
            else:
                self.stdout.write(self.style.SUCCESS(f"Using existing category: {category_name}"))
            
            for product_data in category_data['products']:
                if Product.objects.filter(name=product_data['name']).exists():
                    self.stdout.write(self.style.WARNING(f"Product '{product_data['name']}' already exists, skipping."))
                    continue
                
                product = Product(
                    name=product_data['name'],
                    price=product_data['price'],
                    category=category,
                    description=product_data['description'],
                    stock_quantity=product_data['stock_quantity'],
                    is_sale=product_data['is_sale'],
                    sale_price=product_data['sale_price'],
                    is_in_stock=product_data['stock_quantity'] > 0
                )
                
                try:
                    self.stdout.write(f"Downloading image for {product_data['name']}...")
                    temp_file = download_image(product_data['image_url'])
                    
                    if temp_file:
                        filename = f"{slugify(product_data['name'])}.jpg"
                        
                        with open(temp_file.name, 'rb') as f:
                            product.image.save(filename, File(f), save=False)
                        
                        os.unlink(temp_file.name)
                        
                        self.stdout.write(self.style.SUCCESS(f"Image added for {product_data['name']}"))
                    else:
                        self.stdout.write(self.style.ERROR(f"Failed to download image for {product_data['name']}"))
                except Exception as e:
                    self.stdout.write(self.style.ERROR(f"Error downloading image for {product_data['name']}: {e}"))
                
                product.save()
                self.stdout.write(self.style.SUCCESS(f"Created product: {product_data['name']}"))
        
        self.stdout.write(self.style.SUCCESS('Database seeding completed!'))