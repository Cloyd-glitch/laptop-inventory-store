import os
import django
import urllib.request
from django.core.files.base import ContentFile

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")
django.setup()

from catalog.models import Laptop

# Hardcoded reliable laptop images by brand
BRAND_IMAGES = {
    'Apple': 'https://thumb.wikimedia.org/wikipedia/commons/thumb/9/91/MacBook_Pro_16_%28M1_Pro%2C_2021%29_-_Wikipedia.jpg/960px-MacBook_Pro_16_%28M1_Pro%2C_2021%29_-_Wikipedia.jpg',
    'Dell': 'https://thumb.wikimedia.org/wikipedia/commons/thumb/9/9f/Dell_inspiron.jpg/960px-Dell_inspiron.jpg',
    'Lenovo': 'https://thumb.wikimedia.org/wikipedia/commons/thumb/a/ac/ThinkPad_T14.jpg/960px-ThinkPad_T14.jpg',
    'HP': 'https://thumb.wikimedia.org/wikipedia/commons/thumb/a/ad/HP_Elitebook_820_G4.png/960px-HP_Elitebook_820_G4.png',
    'Acer': 'https://thumb.wikimedia.org/wikipedia/commons/thumb/2/27/Acer_Predator_laptops_and_mice%2C_Computex_Taipei_%2827373087145%29.jpg/960px-Acer_Predator_laptops_and_mice%2C_Computex_Taipei_%2827373087145%29.jpg',
    'ASUS': 'https://upload.wikimedia.org/wikipedia/commons/e/e5/ASUS_Eee_White_Alt.jpg'
}

def update_reliable_images():
    laptops = Laptop.objects.all()
    count = 0
    
    # We will also use the local generated images for MSI and Razer to keep it distinct
    artifact_dir = r"C:\Users\HP\.gemini\antigravity-ide\brain\56055858-9c07-480a-ab0b-02a77c112a39"
    local_images = {
        'MSI': os.path.join(artifact_dir, 'workstation_generic_1789536183083.jpg'),
        'Razer': os.path.join(artifact_dir, 'gaming_laptop_generic_1789536102422.jpg')
    }

    for laptop in laptops:
        # Delete the old image first so we don't bloat
        if laptop.main_image:
            laptop.main_image.delete(save=False)
            
        if laptop.brand in BRAND_IMAGES:
            url = BRAND_IMAGES[laptop.brand]
            try:
                req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
                image_content = urllib.request.urlopen(req).read()
                laptop.main_image.save(f"{laptop.brand}_{laptop.slug}.jpg", ContentFile(image_content), save=True)
                print(f"Updated {laptop.brand} {laptop.model_name} from Wikimedia")
                count += 1
            except Exception as e:
                print(f"Failed to fetch {url}: {e}")
        elif laptop.brand in local_images:
            local_path = local_images[laptop.brand]
            if os.path.exists(local_path):
                with open(local_path, 'rb') as f:
                    laptop.main_image.save(f"{laptop.brand}_{laptop.slug}.jpg", ContentFile(f.read()), save=True)
                print(f"Updated {laptop.brand} {laptop.model_name} from local files")
                count += 1

    print(f"\nSuccessfully assigned {count} reliable laptop images.")

if __name__ == '__main__':
    update_reliable_images()
