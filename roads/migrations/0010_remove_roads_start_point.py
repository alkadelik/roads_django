# Generated by Django 4.0.5 on 2023-03-22 22:07

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('roads', '0009_remove_roads_start_lat_remove_roads_start_lng_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='roads',
            name='start_point',
        ),
    ]
