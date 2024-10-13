import requests
from django.core.management.base import BaseCommand
from store.models import Product

class Command(BaseCommand):
    help = 'Fetch and save products from the API'

    def handle(self, *args, **kwargs):
        response = requests.get('https://dummyjson.com/products')
        if response.status_code == 200:
            products = response.json().get('products', [])
            for product_data in products:
                product, created = Product.objects.update_or_create(
                    id=product_data['id'],
                    defaults={
                        'name': product_data['title'],
                        'price': product_data['price'],
                        'image': product_data['thumbnail']
                    }
                )
                if created:
                    self.stdout.write(self.style.SUCCESS(f'Product {product.name} created'))
                else:
                    self.stdout.write(self.style.WARNING(f'Product {product.name} already exists'))
        else:
            self.stdout.write(self.style.ERROR('Failed to fetch products'))