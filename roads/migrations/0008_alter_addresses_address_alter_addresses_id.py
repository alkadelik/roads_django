# Generated by Django 4.0.5 on 2023-03-22 21:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('roads', '0007_addresses_rename_end_lon_roads_end_lng_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='addresses',
            name='address',
            field=models.CharField(max_length=128, unique=True),
        ),
        migrations.AlterField(
            model_name='addresses',
            name='id',
            field=models.AutoField(primary_key=True, serialize=False),
        ),
    ]
