import requests
from django.core.management.base import BaseCommand
from store.models import Product

# Defining category mapping
CATEGORY_MAPPING = {
    "men's clothing": 'winter',
    "women's clothing": 'summer',
    "jewelery": 'autumn',
    "electronics": 'all_season'
}

class Command(BaseCommand):
    help = 'Fetch and save products from the Fakestore API'

    def handle(self, *args, **kwargs):
        response = requests.get('https://fakestoreapi.com/products')
        if response.status_code == 200:
            products = response.json()
            for product_data in products:
                category = CATEGORY_MAPPING.get(product_data['category'], 'all_season')
                product, created = Product.objects.update_or_create(
                    id=product_data['id'],
                    defaults={
                        'name': product_data['title'],
                        'price': product_data['price'],
                        'image': product_data['image'],
                        'category': category  # Populated category field
                    }
                )
                if created:
                    self.stdout.write(self.style.SUCCESS(f'Product {product.name} created'))
                else:
                    self.stdout.write(self.style.WARNING(f'Product {product.name} already exists'))
        else:
            self.stdout.write(self.style.ERROR('Failed to fetch products'))