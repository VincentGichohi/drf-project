# Generated by Django 4.0.1 on 2022-01-27 13:45

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('watchlist_app', '0003_review'),
    ]

    operations = [
        migrations.RenameField(
            model_name='review',
            old_name='Watchlist',
            new_name='watchlist',
        ),
    ]