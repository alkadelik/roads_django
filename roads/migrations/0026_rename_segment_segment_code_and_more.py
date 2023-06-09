# Generated by Django 4.0.5 on 2023-04-09 09:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('roads', '0025_segment_map'),
    ]

    operations = [
        migrations.RenameField(
            model_name='segment',
            old_name='segment',
            new_name='code',
        ),
        migrations.RenameField(
            model_name='segment',
            old_name='road_name',
            new_name='name',
        ),
        migrations.AddField(
            model_name='segment',
            name='state',
            field=models.CharField(blank=True, max_length=30),
        ),
    ]
