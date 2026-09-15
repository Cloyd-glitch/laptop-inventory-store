import os
import django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")
django.setup()

from django.core.files import File
from catalog.models import Category, Laptop

def seed():
    # 1. Create Categories
    cat_gaming, _ = Category.objects.get_or_create(name='Gaming', slug='gaming')
    cat_ultrabook, _ = Category.objects.get_or_create(name='Ultrabooks', slug='ultrabook')
    cat_workstation, _ = Category.objects.get_or_create(name='Workstations', slug='workstation')

    print("Categories created/verified.")

    artifact_dir = r"C:\Users\HP\.gemini\antigravity-ide\brain\0110880b-44f8-4d22-9521-d6ff31ae8eab"

    # 2. Create Gaming Laptop
    if not Laptop.objects.filter(slug='razer-blade-15').exists():
        laptop1 = Laptop(
            category=cat_gaming,
            brand='Razer',
            model_name='Blade 15',
            slug='razer-blade-15',
            processor='Intel Core i7-13800H',
            ram='16GB DDR5',
            storage='1TB NVMe SSD',
            gpu='NVIDIA GeForce RTX 4070',
            screen_size='15.6 inch QHD 240Hz',
            operating_system='Windows 11 Home',
            condition=Laptop.Condition.NEW,
            price=2499.99,
            stock_quantity=10,
            description='The ultimate gaming laptop with stunning graphics and a sleek CNC aluminum body.',
        )
        img_path = os.path.join(artifact_dir, 'gaming_laptop_1789513476746.jpg')
        if os.path.exists(img_path):
            with open(img_path, 'rb') as f:
                laptop1.main_image.save('gaming_laptop.jpg', File(f), save=False)
        laptop1.save()
        print("Gaming laptop created.")

    # 3. Create Ultrabook
    if not Laptop.objects.filter(slug='dell-xps-13').exists():
        laptop2 = Laptop(
            category=cat_ultrabook,
            brand='Dell',
            model_name='XPS 13',
            slug='dell-xps-13',
            processor='Intel Core i7-1360P',
            ram='16GB LPDDR5',
            storage='512GB PCIe SSD',
            gpu='Intel Iris Xe Graphics',
            screen_size='13.4 inch FHD+',
            operating_system='Windows 11 Pro',
            condition=Laptop.Condition.NEW,
            price=1349.99,
            stock_quantity=15,
            description='Thin, light, and powerful. The XPS 13 is designed for on-the-go productivity.',
        )
        img_path = os.path.join(artifact_dir, 'ultrabook_1789513494596.jpg')
        if os.path.exists(img_path):
            with open(img_path, 'rb') as f:
                laptop2.main_image.save('ultrabook.jpg', File(f), save=False)
        laptop2.save()
        print("Ultrabook created.")

    # 4. Create Workstation
    if not Laptop.objects.filter(slug='lenovo-thinkpad-p16').exists():
        laptop3 = Laptop(
            category=cat_workstation,
            brand='Lenovo',
            model_name='ThinkPad P16',
            slug='lenovo-thinkpad-p16',
            processor='Intel Core i9-12950HX',
            ram='64GB DDR5',
            storage='2TB Performance SSD',
            gpu='NVIDIA RTX A5500 16GB',
            screen_size='16.0 inch WQUXGA',
            operating_system='Windows 11 Pro for Workstations',
            condition=Laptop.Condition.REFURBISHED,
            price=3199.00,
            stock_quantity=5,
            description='A mobile workstation powerhouse built for the most demanding professional workloads.',
        )
        img_path = os.path.join(artifact_dir, 'workstation_1789513511543.jpg')
        if os.path.exists(img_path):
            with open(img_path, 'rb') as f:
                laptop3.main_image.save('workstation.jpg', File(f), save=False)
        laptop3.save()
        print("Workstation created.")

if __name__ == '__main__':
    seed()
