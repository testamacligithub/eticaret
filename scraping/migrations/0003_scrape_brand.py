# Generated by Django 4.0.4 on 2022-10-13 14:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('scraping', '0002_scrape_site_url'),
    ]

    operations = [
        migrations.AddField(
            model_name='scrape',
            name='brand',
            field=models.CharField(max_length=50, null=True),
        ),
    ]