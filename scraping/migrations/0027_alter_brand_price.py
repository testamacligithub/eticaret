# Generated by Django 4.0.4 on 2022-10-20 14:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('scraping', '0026_alter_brand_price_alter_brand_website'),
    ]

    operations = [
        migrations.AlterField(
            model_name='brand',
            name='price',
            field=models.DecimalField(decimal_places=0, max_digits=20),
        ),
    ]
