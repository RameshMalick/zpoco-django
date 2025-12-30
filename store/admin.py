from django.contrib import admin
from django.utils.html import format_html
from unfold.admin import ModelAdmin, TabularInline
from .models import Category, Product, ProductScreenshot, Review

class ProductScreenshotInline(TabularInline):
    model = ProductScreenshot
    extra = 1

class ReviewInline(TabularInline):
    model = Review
    extra = 0

@admin.register(Category)
class CategoryAdmin(ModelAdmin):
    list_display = ("name", "slug")
    prepopulated_fields = {"slug": ("name",)}

@admin.register(Product)
class ProductAdmin(ModelAdmin):
    list_display = ("title", "image_preview", "category", "price", "rating", "is_free", "created_at")
    list_filter = ("category", "rating", "created_at")
    search_fields = ("title", "description")
    inlines = [ProductScreenshotInline, ReviewInline]
    readonly_fields = ("created_at", "updated_at")

    fieldsets = (
        ("General", {
            "fields": ("title", "category", "description")
        }),
        ("Media", {
            "fields": ("image",)
        }),
        ("Pricing & Files", {
            "fields": ("price", "file")
        }),
        ("Call to Action", {
            "fields": ("button_text", "external_link"),
            "description": "Configure the main action button (e.g. 'Download', 'Buy Now') and where it links to."
        }),
        ("Stats & Meta", {
            "fields": ("rating", "created_at", "updated_at"),
            "classes": ("collapse",)
        }),
    )

    def image_preview(self, obj):
        if obj.image:
            return format_html('<img src="{}" style="width: 40px; height: 40px; object-fit: cover; border-radius: 4px;" />', obj.image.url)
        return "-"
    image_preview.short_description = "Image"

@admin.register(Review)
class ReviewAdmin(ModelAdmin):
    list_display = ("author", "product", "rating", "created_at")
