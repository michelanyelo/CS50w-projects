# Generated by Django 5.0.1 on 2024-01-27 13:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0008_listing_bid_current_bid'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='listing',
            name='bid_start',
        ),
        migrations.AlterField(
            model_name='listing',
            name='title',
            field=models.CharField(max_length=100),
        ),
    ]
