# Generated by Django 3.1.3 on 2021-01-06 07:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0010_product_price'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='product',
            name='dob',
        ),
        migrations.RemoveField(
            model_name='product',
            name='pt',
        ),
        migrations.AddField(
            model_name='product',
            name='timedelta',
            field=models.DateField(auto_now_add=True, null=True),
        ),
    ]
