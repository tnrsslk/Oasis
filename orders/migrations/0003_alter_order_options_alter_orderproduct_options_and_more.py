# Generated by Django 5.0 on 2023-12-19 18:39

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0002_alter_order_options_alter_orderproduct_options_and_more'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='order',
            options={'verbose_name': 'Order', 'verbose_name_plural': 'Orders'},
        ),
        migrations.AlterModelOptions(
            name='orderproduct',
            options={'verbose_name': 'Order Product', 'verbose_name_plural': 'Order Products'},
        ),
        migrations.AlterModelOptions(
            name='payment',
            options={'verbose_name': 'Payment', 'verbose_name_plural': 'Payments'},
        ),
    ]