# Generated by Django 4.0.5 on 2023-03-23 07:11

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('roads', '0019_alter_roads_end_point'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='roads',
            name='end_lat',
        ),
        migrations.RemoveField(
            model_name='roads',
            name='end_lng',
        ),
    ]