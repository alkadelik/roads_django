# Generated by Django 4.0.5 on 2023-04-18 10:44

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('roads', '0034_remove_segment_category_route_category'),
    ]

    operations = [
        migrations.CreateModel(
            name='Address',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('address', models.CharField(max_length=256, unique=True)),
                ('name', models.CharField(blank=True, max_length=30)),
                ('lat', models.DecimalField(decimal_places=15, default=0.0, max_digits=30)),
                ('lng', models.DecimalField(decimal_places=15, default=0.0, max_digits=30)),
                ('code', models.CharField(max_length=10)),
            ],
        ),
        migrations.AlterField(
            model_name='segment',
            name='end_point',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='end_point', to='roads.address'),
        ),
        migrations.AlterField(
            model_name='segment',
            name='start_point',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='start_point', to='roads.address'),
        ),
        migrations.DeleteModel(
            name='Addresses',
        ),
    ]
