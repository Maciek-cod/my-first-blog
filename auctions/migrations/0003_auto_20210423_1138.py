# Generated by Django 3.1.2 on 2021-04-23 11:38

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0002_watchlist'),
    ]

    operations = [
        migrations.AddField(
            model_name='bid',
            name='date',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
        migrations.AddField(
            model_name='bid',
            name='listing',
            field=models.ForeignKey(default='0', on_delete=django.db.models.deletion.CASCADE, to='auctions.listing'),
        ),
        migrations.AddField(
            model_name='bid',
            name='user',
            field=models.ForeignKey(default='0', on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]