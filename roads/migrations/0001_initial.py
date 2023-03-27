# Generated by Django 4.0.5 on 2023-03-15 08:14

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Roads',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('route_no', models.CharField(default='A00', max_length=10)),
                ('segment_no', models.CharField(default='A00', max_length=10)),
                ('start_lat', models.DecimalField(decimal_places=15, default=0.0, max_digits=30)),
                ('start_lon', models.DecimalField(decimal_places=15, default=0.0, max_digits=30)),
                ('end_lat', models.DecimalField(decimal_places=15, default=0.0, max_digits=30)),
                ('end_lon', models.DecimalField(decimal_places=15, default=0.0, max_digits=30)),
                ('road_name', models.CharField(blank=True, max_length=24)),
                ('distance', models.DecimalField(decimal_places=2, default=0, max_digits=5)),
                ('travel_time', models.IntegerField(default=0, max_length=2)),
                ('avg_speed', models.DecimalField(decimal_places=1, default=0.0, max_digits=4)),
                ('road_condition', models.IntegerField(default=0)),
            ],
        ),
    ]