# Generated by Django 2.2.7 on 2019-12-09 13:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0007_auto_20191209_1328'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='item',
            name='cart_quantity',
        ),
        migrations.AddField(
            model_name='orderitem',
            name='order_quantity',
            field=models.IntegerField(default=1),
        ),
    ]
