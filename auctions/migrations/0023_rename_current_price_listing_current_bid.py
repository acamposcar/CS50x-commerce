# Generated by Django 4.0.2 on 2022-02-28 12:12

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0022_rename_starting_bid_listing_starting_price_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='listing',
            old_name='current_price',
            new_name='current_bid',
        ),
    ]
