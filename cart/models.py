from django.db import models
from shop.models import Product
from shop.models import Variation
from accounts.models import Account


class Cart(models.Model):
    cart_id = models.CharField(max_length=250, blank=True)
    create = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.cart_id

    class Meta:
        verbose_name = 'Cart'
        verbose_name_plural = 'Carts'


class CartItem(models.Model):
    # Пользователь, которому принадлежит корзина, может быть пустым для неавторизованных пользователей
    user = models.ForeignKey(Account, on_delete=models.CASCADE, null=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    # Вариации продукта, если они есть
    variation = models.ManyToManyField(Variation, blank=True)
    # Ссылка на корзину, к которой относится товар
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, null=True)
    # Количество единиц товара в корзине
    quantity = models.IntegerField(default=0)
    # Флаг активности товара в корзине
    is_active = models.BooleanField(default=True)


    def sub_total(self):
        return self.product.price * self.quantity

    def __unicode__(self):
        return self.product

    class Meta:
        verbose_name = 'Cart Item'
        verbose_name_plural = 'Cart Items'
