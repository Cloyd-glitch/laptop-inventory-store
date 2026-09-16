import os
import django
import random

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")
django.setup()

from django.core.files import File
from catalog.models import Laptop

def assign_images():
    artifact_dir = r"C:\Users\HP\.gemini\antigravity-ide\brain\56055858-9c07-480a-ab0b-02a77c112a39"
    
    images = [
        os.path.join(artifact_dir, 'gaming_laptop_generic_1789536102422.jpg'),
        os.path.join(artifact_dir, 'ultrabook_generic_1789536170215.jpg'),
        os.path.join(artifact_dir, 'workstation_generic_1789536183083.jpg')
    ]
    
    valid_images = [img for img in images if os.path.exists(img)]
    
    if not valid_images:
        print("No images found to assign.")
        return

    laptops_without_images = Laptop.objects.filter(main_image='')
    count = 0
    
    for laptop in laptops_without_images:
        img_path = random.choice(valid_images)
        with open(img_path, 'rb') as f:
            laptop.main_image.save(f'generic_{laptop.pk}.jpg', File(f), save=True)
        count += 1
        
    print(f"Assigned images to {count} laptops.")

if __name__ == '__main__':
    assign_images()
