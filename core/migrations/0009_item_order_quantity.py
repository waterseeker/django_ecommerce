# Generated by Django 2.2.7 on 2019-12-09 14:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0008_auto_20191209_1337'),
    ]

    operations = [
        migrations.AddField(
            model_name='item',
            name='order_quantity',
            field=models.IntegerField(default=9000),
        ),
    ]