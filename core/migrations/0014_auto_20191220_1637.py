# Generated by Django 3.0 on 2019-12-20 16:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0013_billingaddress'),
    ]

    operations = [
        migrations.AlterField(
            model_name='billingaddress',
            name='zip',
            field=models.CharField(max_length=100),
        ),
    ]
