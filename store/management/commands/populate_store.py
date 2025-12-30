from django.core.management.base import BaseCommand
from store.models import Category, Product
import random

class Command(BaseCommand):
    help = 'Populates the store with demo content'

    def handle(self, *args, **kwargs):
        self.stdout.write('Populating store data...')

        # defined text-based icons for categories
        # Note: In a real app we might use image fields, but for this text-base icon is fine for the header 
        # or we rely on the template to map slugs to icons, but let's just ensure categories exist.
        
        categories_data = [
            {'name': 'Games', 'slug': 'games', 'icon': '🎮'},
            {'name': 'Apps', 'slug': 'apps', 'icon': '📱'},
            {'name': 'eBooks', 'slug': 'ebooks', 'icon': '📚'},
            {'name': 'Worksheets', 'slug': 'worksheets', 'icon': '📝'},
        ]

        categories = {}
        for cat_data in categories_data:
            cat, created = Category.objects.get_or_create(
                slug=cat_data['slug'],
                defaults={'name': cat_data['name']}
            )
            categories[cat.slug] = cat
            if created:
                self.stdout.write(f"Created category: {cat.name}")

        # Demo Products
        demo_products = [
            # Games
            {'title': 'Cosmic Racer', 'cat': 'games', 'price': 0, 'rating': 4.8},
            {'title': 'Kingdom Defense', 'cat': 'games', 'price': 4.99, 'rating': 4.9},
            {'title': 'Puzzle Master 3D', 'cat': 'games', 'price': 0, 'rating': 4.5},
            {'title': 'Speed Legends', 'cat': 'games', 'price': 2.99, 'rating': 4.6},
            {'title': 'Pixel Quest', 'cat': 'games', 'price': 0, 'rating': 4.2},
            
            # Apps
            {'title': 'Focus Timer Pro', 'cat': 'apps', 'price': 1.99, 'rating': 4.9},
            {'title': 'Daily Yoga', 'cat': 'apps', 'price': 0, 'rating': 4.7},
            {'title': 'Budget Tracker', 'cat': 'apps', 'price': 0, 'rating': 4.4},
            {'title': 'Photo Editor X', 'cat': 'apps', 'price': 3.99, 'rating': 4.5},
            {'title': 'Secure Notes', 'cat': 'apps', 'price': 0.99, 'rating': 4.8},

            # eBooks
            {'title': 'Mastering Python', 'cat': 'ebooks', 'price': 9.99, 'rating': 5.0},
            {'title': 'Sci-Fi Looking Glass', 'cat': 'ebooks', 'price': 4.99, 'rating': 4.3},
            {'title': 'Healthy Cooking 101', 'cat': 'ebooks', 'price': 0, 'rating': 4.6},
            {'title': 'Space History', 'cat': 'ebooks', 'price': 0, 'rating': 4.7},
            {'title': 'The Art of Design', 'cat': 'ebooks', 'price': 12.99, 'rating': 4.9},

            # Worksheets
            {'title': 'Math Grade 1 Practice', 'cat': 'worksheets', 'price': 0, 'rating': 4.5},
            {'title': 'Science Lab Report', 'cat': 'worksheets', 'price': 1.00, 'rating': 4.8},
            {'title': 'Geography World Map', 'cat': 'worksheets', 'price': 0, 'rating': 4.4},
            {'title': 'Grammar Basics', 'cat': 'worksheets', 'price': 0, 'rating': 4.2},
            {'title': 'Alphabet Coloring', 'cat': 'worksheets', 'price': 0, 'rating': 5.0},
        ]

        for prod_data in demo_products:
            cat = categories[prod_data['cat']]
            title = prod_data['title']
            
            if not Product.objects.filter(title=title).exists():
                Product.objects.create(
                    title=title,
                    category=cat,
                    description=f"This is a demo description for {title}. Experience the best in {cat.name} with this amazing item.",
                    price=prod_data['price'],
                    rating=prod_data['rating'],
                    # Optional: Add external link or default button text
                    button_text="Get It" if prod_data['price'] == 0 else "Buy Now",
                )
                self.stdout.write(f"Created product: {title}")
            else:
                self.stdout.write(f"Skipped existing: {title}")

        self.stdout.write(self.style.SUCCESS('Successfully populated store with demo content!'))
