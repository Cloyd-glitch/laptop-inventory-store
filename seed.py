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

    # 5. Create 50+ More Random Laptops
    import random
    from django.utils.text import slugify

    cat_business, _ = Category.objects.get_or_create(name='Business', slug='business')
    cat_budget, _ = Category.objects.get_or_create(name='Budget', slug='budget')
    
    categories = [cat_gaming, cat_ultrabook, cat_workstation, cat_business, cat_budget]
    brands = ['Dell', 'HP', 'Lenovo', 'ASUS', 'Acer', 'Apple', 'MSI', 'Razer']
    processors = ['Intel Core i5-12400', 'Intel Core i7-13700H', 'Intel Core i9-13900HX', 'AMD Ryzen 5 7600', 'AMD Ryzen 7 7800X3D', 'Apple M2', 'Apple M3 Pro']
    gpus = ['Integrated Graphics', 'Intel Iris Xe', 'NVIDIA GTX 1650', 'NVIDIA RTX 3060', 'NVIDIA RTX 4070', 'AMD Radeon RX 7600M']
    rams = ['8GB DDR4', '16GB DDR5', '32GB DDR5', '64GB DDR5']
    storages = ['256GB SSD', '512GB SSD', '1TB NVMe SSD', '2TB NVMe SSD']
    conditions = [Laptop.Condition.NEW, Laptop.Condition.USED, Laptop.Condition.REFURBISHED]

    created_count = 0
    for i in range(1, 51):
        brand = random.choice(brands)
        model = f"ProBook {random.randint(1000, 9000)}" if brand == 'HP' else \
                f"ThinkPad T{random.randint(14, 16)}" if brand == 'Lenovo' else \
                f"ZenBook {random.randint(13, 15)}" if brand == 'ASUS' else \
                f"MacBook Pro {random.randint(13, 16)}" if brand == 'Apple' else \
                f"Inspiron {random.randint(3000, 7000)}" if brand == 'Dell' else \
                f"Predator {random.randint(300, 700)}" if brand == 'Acer' else \
                f"Stealth {random.randint(14, 17)}" if brand == 'MSI' else \
                f"Blade {random.randint(14, 18)}"
                
        slug = slugify(f"{brand}-{model}-{i}")
        
        if not Laptop.objects.filter(slug=slug).exists():
            laptop = Laptop(
                category=random.choice(categories),
                brand=brand,
                model_name=model,
                slug=slug,
                processor=random.choice(processors),
                ram=random.choice(rams),
                storage=random.choice(storages),
                gpu=random.choice(gpus),
                screen_size=f"{random.choice([13.3, 14.0, 15.6, 16.0, 17.3])} inch",
                operating_system='Windows 11' if brand != 'Apple' else 'macOS',
                condition=random.choice(conditions),
                price=round(random.uniform(20000, 150000), 2),
                stock_quantity=random.randint(0, 25),
                description=f'A highly capable {brand} laptop suitable for various tasks.',
                is_active=True
            )
            
            # Assign custom distinct placeholder
            import urllib.request
            from django.core.files.base import ContentFile
            
            # Using LoremFlickr to get real laptop images
            # Using the laptop id/pk as a lock to ensure a consistent, unique image for this laptop
            laptop.save() # Save first so it has an ID
            
            url = f"https://loremflickr.com/800/600/laptop?lock={laptop.pk}"
            
            try:
                req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
                response = urllib.request.urlopen(req)
                image_content = response.read()
                laptop.main_image.save(f"real_{laptop.slug}.jpg", ContentFile(image_content), save=True)
            except Exception as e:
                print(f"Warning: Failed to fetch image for {laptop.slug}: {e}")
                    
            created_count += 1

    print(f"{created_count} random laptops created.")

if __name__ == '__main__':
    seed()
