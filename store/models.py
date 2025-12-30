from django.db import models

class Category(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True)
    icon = models.CharField(max_length=50, default="box", help_text="Lucide icon name or image url")

    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name_plural = "Categories"

class Product(models.Model):
    title = models.CharField(max_length=200)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name="products")
    description = models.TextField()
    price = models.DecimalField(max_digits=6, decimal_places=2, null=True, blank=True, help_text="Null for Free")
    rating = models.DecimalField(max_digits=3, decimal_places=1, default=0.0)
    reviews_count = models.IntegerField(default=0)
    image = models.ImageField(upload_to="products/images/", null=True, blank=True)
    file = models.FileField(upload_to="products/files/", null=True, blank=True)
    version = models.CharField(max_length=20, default="1.0.0")
    size = models.CharField(max_length=20, default="10 MB")
    updated_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)
    external_link = models.URLField(blank=True, null=True, help_text="Link for 'Buy/Click' button")
    button_text = models.CharField(max_length=50, default="Click Here", help_text="Text for the action button")

    def __str__(self):
        return self.title

    @property
    def is_free(self):
        return self.price is None or self.price == 0

class ProductScreenshot(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="screenshots")
    image = models.ImageField(upload_to="products/screenshots/")

    def __str__(self):
        return f"Screenshot for {self.product.title}"

class Review(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="reviews")
    author = models.CharField(max_length=100)
    rating = models.IntegerField(default=5)
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.author} - {self.product.title}"
