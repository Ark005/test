# Generated by Django 3.0.6 on 2021-01-07 17:27

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('cart', '0001_initial'),
        ('products', '0019_auto_20210107_2003'),
    ]

    operations = [
        migrations.DeleteModel(
            name='BoxType1',
        ),
        migrations.CreateModel(
            name='BoxType1',
            fields=[
            ],
            options={
                'proxy': True,
                'indexes': [],
                'constraints': [],
            },
            bases=('products.product',),
        ),
    ]