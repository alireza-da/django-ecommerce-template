import uuid
from datetime import datetime

from django.db import models

from registration.models import CustomUser, UserAddress


# Create your models here.
class Category(models.Model):
    name = models.CharField(max_length=255)
    parent_id = models.ForeignKey('self', on_delete=models.SET_NULL, null=True)
    description = models.TextField()
    deleted_at = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


class Product(models.Model):
    name = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255, unique=True)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True)
    primary_image = models.ImageField()
    description = models.TextField()
    price = models.DecimalField(max_digits=20, decimal_places=2)
    quantity = models.IntegerField(default=0)
    status = models.IntegerField(default=0)
    sale_price = models.DecimalField(max_digits=20, decimal_places=2, default=0, null=True)
    date_on_sale_from = models.DateField(null=True)
    date_on_sale_to = models.DateField(null=True)
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, null=True)
    deleted_at = models.DateTimeField(null=True)

    def __str__(self):
        return self.name


class ProductImage(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='product')
    image = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    deleted_at = models.DateTimeField(null=True)


class Coupon(models.Model):
    code = models.CharField(default="", max_length=255)
    percentage = models.FloatField(default=0)
    expired_at = models.DateTimeField(null=True)
    deleted_at = models.DateTimeField(null=True)
    created_at = models.DateTimeField(default=datetime.now(), null=True)
    updated_at = models.DateTimeField(default=datetime.now(), null=True)

    def __str__(self):
        return f"Coupon({self.code}, {self}"


class Payment(models.Model):
    total_amount = models.FloatField(default=0)
    coupon_amount = models.FloatField(default=0)
    paying_amount = models.FloatField(default=0)
    payment_status = models.IntegerField(default=0)
    coupon_id = models.ForeignKey(to=Coupon, on_delete=models.SET_NULL, null=True)


class Order(models.Model):
    """
    Order model
    status: int = 0 default submit not processed, 1 = processed pending order, 2 completed
    """
    order_id = models.UUIDField(default=uuid.uuid4)
    payment = models.ForeignKey(to=Payment, on_delete=models.CASCADE)
    user = models.ForeignKey(to=CustomUser, on_delete=models.SET_NULL, null=True)
    address = models.ForeignKey(to=UserAddress, on_delete=models.SET_NULL, null=True)
    status = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    deleted_at = models.DateTimeField(null=True)

    def __str__(self):
        return f"Order({self}"

    def __str__(self):
        return f"OrderItem({self.order}, {self.product}, {self.price}, {self}"


class OrderItem(models.Model):
    product = models.ForeignKey(to=Product, on_delete=models.SET_NULL, null=True, blank=True, related_name="product_ref")
    price = models.FloatField(default=0)
    order = models.ForeignKey(to=Order, on_delete=models.CASCADE, null=True)
    quantity = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    deleted_at = models.DateTimeField(null=True)


class Transaction(models.Model):
    user = models.ForeignKey(to=CustomUser, on_delete=models.SET_NULL, null=True)
    transaction_id = models.UUIDField(default=uuid.uuid4)
    code = models.CharField(max_length=255, null=True, blank=True)
    payment = models.ForeignKey(to=Payment, on_delete=models.SET_NULL, null=True)
    amount = models.FloatField(default=0)
    token = models.CharField(max_length=255, default="", blank=True)
    status = models.IntegerField(default=0) # 0 = success, 1 = pending , 2 = error
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    deleted_at = models.DateTimeField(null=True)
