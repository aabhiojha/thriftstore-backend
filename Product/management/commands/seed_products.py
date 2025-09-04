import random
from decimal import Decimal
from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from Product.models import Category, Product

CONDITIONS = ["new", "like_new", "good", "fair", "poor"]

CATEGORY_NAMES = [
    "Clothing", "Electronics", "Books", "Home Decor", "Furniture",
    "Toys", "Sports", "Jewelry", "Kitchen", "Art"
]

class Command(BaseCommand):
    help = "Seed 10 categories and 100 sample products"

    def handle(self, *args, **options):
        User = get_user_model()

        # Get or create a seller user
        seller = User.objects.order_by("id").first()
        if not seller:
            seller = User.objects.create_user(
                username="demo_seller",
                password="password123",
                email="demo_seller@example.com"
            )
            self.stdout.write(self.style.WARNING("Created demo seller user (demo_seller/password123)"))

        # Categories
        categories = []
        for name in CATEGORY_NAMES:
            cat, _ = Category.objects.get_or_create(name=name, defaults={"description": f"{name} items"})
            categories.append(cat)

        created = 0
        for i in range(1, 101):
            cat = random.choice(categories)
            price = Decimal(random.randrange(200, 20000)) / 100  # 2.00 - 200.00
            condition = random.choice(CONDITIONS)
            is_featured = (i % 15 == 0)
            p, made = Product.objects.get_or_create(
                name=f"Sample Product {i}",
                defaults={
                    "description": f"Description for sample product {i} in {cat.name}.",
                    "price": price,
                    "condition": condition,
                    "seller": seller,
                    "is_available": True,
                    "category": cat,
                    "is_featured": is_featured,
                    "views_count": random.randint(0, 500),
                },
            )
            if made:
                created += 1

        self.stdout.write(self.style.SUCCESS(f"Seed complete. Products created: {created}"))