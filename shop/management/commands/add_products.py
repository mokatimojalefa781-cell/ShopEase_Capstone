# shop/management/commands/add_products.py

from django.core.management.base import BaseCommand
from shop.models import Product
import os
from django.conf import settings

class Command(BaseCommand):
    help = 'Add predefined products with images'

    def handle(self, *args, **options):
        # Your product list
        products_data = [
            'burger', 'cake', 'coffe', 'donut', 'fries',
            'ice creame', 'pizza', 'salad', 'sandwitch', 'soda'
        ]

        for name in products_data:
            try:
                product = Product.objects.get(name=name)
                self.stdout.write(f"Product '{name}' already exists.")
            except Product.DoesNotExist:
                # Build the image file path (replace spaces with underscores if needed)
                image_file = f"products/{name.replace(' ', '_')}.jpg"
                image_path = os.path.join(settings.MEDIA_ROOT, image_file)

                if not os.path.exists(image_path):
                    self.stdout.write(f"Image '{image_file}' does not exist! Skipping product '{name}'.")
                    continue

                # Create the product
                product = Product.objects.create(
                    name=name,
                    price=0,  # Set default price 0; you can update later
                    image=image_file
                )
                self.stdout.write(f"Product '{name}' created successfully with image '{image_file}'.")
