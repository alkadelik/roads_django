# Generated by Django 4.0.5 on 2023-03-15 08:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('roads', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='roads',
            name='travel_time',
            field=models.IntegerField(default=0),
        ),
    ]
