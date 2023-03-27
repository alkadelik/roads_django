# Generated by Django 4.0.5 on 2023-03-23 07:07

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('roads', '0017_alter_roads_start_point'),
    ]

    operations = [
        migrations.AlterField(
            model_name='roads',
            name='start_point',
            field=models.ForeignKey(default=14, on_delete=django.db.models.deletion.SET_DEFAULT, related_name='start_point', to='roads.addresses', to_field='address'),
        ),
    ]