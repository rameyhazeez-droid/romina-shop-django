from django.db import models
from cloudinary.models import CloudinaryField


class Product(models.Model):
    product_id = models.AutoField(primary_key=True)
    product_name = models.CharField(max_length=50)
    category = models.CharField(max_length=50, default="")
    subcategory = models.CharField(max_length=50, default="")
    price = models.IntegerField(default=0)
    desc = models.TextField(max_length=1000)
    pub_date = models.DateField()
    # CloudinaryField handles uploads and accepts a folder path
    image = CloudinaryField('image', folder='shop/images', default="")

    def __str__(self):
        return self.product_name

    # Note: Custom local cropping in the save method is removed because
    # Cloudinary handles cropping and optimization dynamically on-the-fly via URLs!


class ProductImage(models.Model):
    product = models.ForeignKey(
        Product, default=None, on_delete=models.CASCADE, related_name="images"
    )
    image = CloudinaryField('image', folder='shop/images', default="")

    def __str__(self):
        return f"Image for {self.product.product_name}"


class SiteBanner(models.Model):
    title = models.CharField(max_length=100, default="Romina Creation Story")
    image = CloudinaryField('image', folder='shop/images', default="")
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return str(self.title)


class Contact(models.Model):
    msg_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=70)
    email = models.CharField(max_length=70, default="")
    phone = models.CharField(max_length=70, default="")
    desc = models.CharField(max_length=500, default="")

    def __str__(self):
        return self.name


class Order(models.Model):
    order_id = models.AutoField(primary_key=True)
    items_json = models.CharField(max_length=5000)
    amount = models.IntegerField(default=0)
    name = models.CharField(max_length=132)
    email = models.CharField(max_length=132)
    address = models.CharField(max_length=132)
    city = models.CharField(max_length=132)
    zip_code = models.CharField(max_length=132)
    desc = models.CharField(max_length=300, default="")
    phone = models.CharField(max_length=111)

    def __str__(self):
        return f"Order #{self.order_id} - {self.name}"


class OrderUpdate(models.Model):
    update_id = models.AutoField(primary_key=True)
    order_id = models.IntegerField(default=0)
    update_desc = models.CharField(max_length=5000)
    timestamp = models.DateTimeField(auto_now_add=True)  # Includes date AND time

    def __str__(self):
        desc = self.update_desc or ""
        return f"Order #{self.order_id}: {desc[:15]}..."