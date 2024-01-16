# Generated by Django 5.0 on 2023-12-20 18:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0004_alter_payment_payment_method'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='orderproduct',
            name='payment',
        ),
        migrations.RemoveField(
            model_name='order',
            name='payment',
        ),
        migrations.AlterField(
            model_name='order',
            name='state',
            field=models.CharField(max_length=100),
        ),
        migrations.DeleteModel(
            name='Payment',
        ),
    ]
