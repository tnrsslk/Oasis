from django.db import models
from accounts.models import Account
from shop.models import Product, Variation
import uuid


class Order(models.Model):
    # Модель для хранения информации о заказе
    STATUS = (
        ('New', 'New'),
        ('Accepted', 'Accepted'),
        ('Completed', 'Completed'),
        ('Cancelled', 'Cancelled'),
    )

    user = models.ForeignKey(Account, on_delete=models.SET_NULL, null=True)
    order_id = models.CharField(max_length=36, unique=True)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    phone = models.CharField(max_length=15)
    email = models.EmailField(max_length=50)
    address = models.TextField(max_length=1000)
    country = models.CharField(max_length=50)
    state = models.CharField(max_length=100)
    city = models.CharField(max_length=50)
    order_note = models.CharField(max_length=1000, blank=True)
    order_total = models.FloatField()
    tax = models.FloatField()
    status = models.CharField(max_length=10, choices=STATUS, default='New')
    ip = models.CharField(blank=True, max_length=20)
    is_ordered = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    paid = models.BooleanField(default=False)

    def full_name(self):
        return f'{self.first_name} {self.last_name}'

    def order_created(self):
        return self.created_at.strftime('%B %d %Y')

    def hour_update(self):
        return self.created_at.strftime('%H:%M %p')

    def __str__(self):
        return self.first_name

    class Meta:
        verbose_name = 'Order'
        verbose_name_plural = 'Orders'


class OrderProduct(models.Model):
    # Модель для хранения информации о продуктах в заказе
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    user = models.ForeignKey(Account, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    variations = models.ManyToManyField(Variation, blank=True)
    quantity = models.IntegerField()
    product_price = models.FloatField()
    ordered = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def sub_total(self):
        return self.quantity * self.product_price

    def order_created(self):
        return self.created_at.strftime('%B %d %Y')

    def __str__(self):
        return self.product.name

    class Meta:
        verbose_name = 'Order Product'
        verbose_name_plural = 'Order Products'