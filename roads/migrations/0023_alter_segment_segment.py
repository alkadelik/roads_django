# Generated by Django 4.0.5 on 2023-03-30 21:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('roads', '0022_alter_route_route'),
    ]

    operations = [
        migrations.AlterField(
            model_name='segment',
            name='segment',
            field=models.CharField(max_length=10, unique=True),
        ),
    ]
