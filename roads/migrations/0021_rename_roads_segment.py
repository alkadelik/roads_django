# Generated by Django 4.0.5 on 2023-03-30 17:48

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('roads', '0020_remove_roads_end_lat_remove_roads_end_lng'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Roads',
            new_name='Segment',
        ),
    ]