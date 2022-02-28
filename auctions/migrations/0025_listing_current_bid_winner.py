# Generated by Django 4.0.2 on 2022-02-28 12:22

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0024_alter_listing_current_bid'),
    ]

    operations = [
        migrations.AddField(
            model_name='listing',
            name='current_bid_winner',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='bid_winner', to=settings.AUTH_USER_MODEL),
        ),
    ]
