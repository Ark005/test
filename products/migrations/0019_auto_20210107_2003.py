# Generated by Django 3.0.6 on 2021-01-07 17:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0018_auto_20210107_1954'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='box_size',
            field=models.CharField(choices=[('50х50х35', '50х50х35')], default='80х80х40', max_length=20),
        ),
    ]