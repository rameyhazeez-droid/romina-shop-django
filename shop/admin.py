from django.contrib import admin
from .models import Contact, Order, OrderUpdate, Product, ProductImage, SiteBanner


# 1. Define your inline for multiple product images
class ProductImageAdmin(admin.TabularInline):
    model = ProductImage
    extra = 4


# 2. Define your custom admin class incorporating the inline
class ProductAdmin(admin.ModelAdmin):
    inlines = [ProductImageAdmin]


# 3. Register your models safely (each registered exactly once)
admin.site.register(Product, ProductAdmin)
admin.site.register(SiteBanner)
admin.site.register(Contact)
admin.site.register(Order)
admin.site.register(OrderUpdate)