# Generated by Django 4.0.5 on 2023-04-05 08:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('roads', '0024_alter_segment_route_alter_segment_status'),
    ]

    operations = [
        migrations.AddField(
            model_name='segment',
            name='map',
            field=models.ImageField(blank=True, upload_to='images'),
        ),
    ]
