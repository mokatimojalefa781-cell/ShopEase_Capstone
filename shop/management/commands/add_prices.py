# shop/management/commands/add_prices.py

from django.core.management.base import BaseCommand
from shop.models import Product

class Command(BaseCommand):
    help = 'Set prices for products'

    def handle(self, *args, **options):
        # Define prices for your products
        product_prices = {
            'burger': 50,
            'cake': 80,
            'coffe': 30,
            'donut': 25,
            'fries': 20,
            'ice creame': 40,
            'pizza': 120,
            'salad': 60,
            'sandwitch': 45,
            'soda': 15,
        }

        for name, price in product_prices.items():
            try:
                product = Product.objects.get(name=name)
                product.price = price
                product.save()
                self.stdout.write(f"Updated '{name}' price to {price}.")
            except Product.DoesNotExist:
                self.stdout.write(f"Product '{name}' does not exist. Skipping.")
