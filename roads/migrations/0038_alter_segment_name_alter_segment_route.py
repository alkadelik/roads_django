# Generated by Django 4.0.5 on 2023-04-18 13:44

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('roads', '0037_remove_address_code'),
    ]

    operations = [
        migrations.AlterField(
            model_name='segment',
            name='name',
            field=models.CharField(blank=True, max_length=64),
        ),
        migrations.AlterField(
            model_name='segment',
            name='route',
            field=models.ForeignKey(db_column='route', default=1, on_delete=django.db.models.deletion.PROTECT, to='roads.route'),
        ),
    ]