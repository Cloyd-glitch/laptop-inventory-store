import os
import django
import urllib.request
import urllib.parse
from django.core.files.base import ContentFile

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")
django.setup()

from catalog.models import Laptop

def update_placeholders():
    laptops = Laptop.objects.all()
    count = 0
    
    for laptop in laptops:
        # We want to replace the generic ones and any missing ones
        if not laptop.main_image or 'generic' in laptop.main_image.name or 'picsum' in laptop.main_image.name:
            # Create a custom placeholder with the laptop's exact name and brand
            # Using the colors from our design system: Background #2a2a2c, Text #c98a4b
            text = f"{laptop.brand}\n{laptop.model_name}"
            encoded_text = urllib.parse.quote(text)
            url = f"https://placehold.co/800x600/2a2a2c/c98a4b.png?text={encoded_text}"
            
            try:
                # Add a user-agent to avoid being blocked
                req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
                response = urllib.request.urlopen(req)
                image_content = response.read()
                
                # Save the new distinct image
                filename = f"placeholder_{laptop.slug}.png"
                
                # Delete old image if it exists to avoid bloat
                if laptop.main_image:
                    laptop.main_image.delete(save=False)
                    
                laptop.main_image.save(filename, ContentFile(image_content), save=True)
                count += 1
                print(f"Assigned distinct placeholder to {laptop.brand} {laptop.model_name}")
            except Exception as e:
                print(f"Failed for {laptop.slug}: {e}")
                
    print(f"\nSuccessfully generated {count} distinct brand images.")

if __name__ == '__main__':
    update_placeholders()
