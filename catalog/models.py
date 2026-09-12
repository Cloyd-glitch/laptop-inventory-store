from django.db import models
from django.utils.text import slugify


class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(max_length=120, unique=True, blank=True)

    class Meta:
        verbose_name_plural = 'Categories'
        ordering = ['name']

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name


class Laptop(models.Model):
    class Condition(models.TextChoices):
        NEW = 'NEW', 'Brand New'
        USED = 'USED', 'Used'
        REFURBISHED = 'REFURB', 'Refurbished'

    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, related_name='laptops')
    brand = models.CharField(max_length=50)
    model_name = models.CharField(max_length=100)
    slug = models.SlugField(max_length=150, unique=True, blank=True)

    # Specs
    processor = models.CharField(max_length=100)
    ram = models.CharField(max_length=50, help_text="e.g. 16GB DDR5")
    storage = models.CharField(max_length=50, help_text="e.g. 512GB SSD")
    gpu = models.CharField(max_length=100, blank=True)
    screen_size = models.CharField(max_length=20, help_text="e.g. 15.6 inch")
    operating_system = models.CharField(max_length=50, blank=True)

    condition = models.CharField(max_length=10, choices=Condition.choices, default=Condition.NEW)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    stock_quantity = models.PositiveIntegerField(default=0)

    main_image = models.ImageField(upload_to='laptops/main/')
    description = models.TextField(blank=True)

    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(f"{self.brand}-{self.model_name}")
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.brand} {self.model_name}"

    @property
    def in_stock(self):
        return self.stock_quantity > 0


class LaptopImage(models.Model):
    laptop = models.ForeignKey(Laptop, on_delete=models.CASCADE, related_name='gallery_images')
    image = models.ImageField(upload_to='laptops/gallery/')
    caption = models.CharField(max_length=100, blank=True)

    def __str__(self):
        return f"Image for {self.laptop}"