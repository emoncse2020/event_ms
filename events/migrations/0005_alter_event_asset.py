# Generated by Django 5.1.7 on 2025-03-27 01:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0004_event_asset'),
    ]

    operations = [
        migrations.AlterField(
            model_name='event',
            name='asset',
            field=models.ImageField(blank=True, default='events_asset/def_img.jpeg', null=True, upload_to='events_asset'),
        ),
    ]
