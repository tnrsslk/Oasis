from django.db import models
from shop.models import Product
from shop.models import Variation
from accounts.models import Account


class Wishlist(models.Model):
    user = models.ForeignKey(Account, on_delete=models.CASCADE, null=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    # Вариации товара (если есть)
    variation = models.ManyToManyField(Variation, blank=True)
    # Дата и время добавления элемента в избранное (устанавливается автоматически при создании)
    added_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user} - {self.product}"


    class Meta:
        verbose_name = 'Wishlist'
        verbose_name_plural = 'Wishlists'
