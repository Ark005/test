# Generated by Django 3.1.3 on 2021-02-10 13:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0048_auto_20210210_1232'),
    ]

    operations = [
        migrations.AddField(
            model_name='boxsizes',
            name='lim1',
            field=models.FloatField(default=None, null=True),
        ),
        migrations.AddField(
            model_name='boxsizes',
            name='lim2',
            field=models.FloatField(default=None, null=True),
        ),
    ]