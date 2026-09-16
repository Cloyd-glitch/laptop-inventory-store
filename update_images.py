import os
import django
import urllib.request
from django.core.files.base import ContentFile

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")
django.setup()

from catalog.models import Laptop

def update_real_images():
    laptops = Laptop.objects.all()
    count = 0
    
    for laptop in laptops:
        # Update if it's a placeholder or generic
        if not laptop.main_image or 'placeholder' in laptop.main_image.name or 'generic' in laptop.main_image.name:
            # Use loremflickr with the laptop keyword. 
            # The lock parameter ensures a consistent but distinct random image per laptop ID.
            url = f"https://loremflickr.com/800/600/laptop?lock={laptop.pk}"
            
            try:
                # Add a user-agent to avoid being blocked
                req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
                response = urllib.request.urlopen(req)
                image_content = response.read()
                
                # Save the new real image
                filename = f"real_{laptop.slug}.jpg"
                
                # Delete old image if it exists
                if laptop.main_image:
                    laptop.main_image.delete(save=False)
                    
                laptop.main_image.save(filename, ContentFile(image_content), save=True)
                count += 1
                print(f"Assigned real image to {laptop.brand} {laptop.model_name}")
            except Exception as e:
                print(f"Failed for {laptop.slug}: {e}")
                
    print(f"\nSuccessfully downloaded {count} real laptop images.")

if __name__ == '__main__':
    update_real_images()
