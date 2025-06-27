from django.db import models


class Product(models.Model):
    name = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    image = models.ImageField(upload_to='products/')
    description = models.TextField(blank=True)
    is_latest = models.BooleanField(default=False)  # ✅ New field
    is_offer = models.BooleanField(default=False)  # ✅ For Offer Zone


    def __str__(self):
        return self.name


class Order(models.Model):
    full_name = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=15)
    address = models.TextField()
    product_name = models.CharField(max_length=100)
    quantity = models.PositiveIntegerField()
    otp = models.IntegerField()
    order_date = models.DateTimeField(auto_now_add=True)
    payment_id = models.CharField(max_length=100, null=True, blank=True)

    def __str__(self):
        return f"Order by {self.full_name} for {self.product_name}"

class ContactMessage(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=15)
    subject = models.CharField(max_length=255)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name
