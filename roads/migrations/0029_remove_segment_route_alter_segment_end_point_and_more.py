# Generated by Django 4.0.5 on 2023-04-10 19:09

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('roads', '0028_alter_segment_end_point_alter_segment_start_point'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='segment',
            name='route',
        ),
        migrations.AlterField(
            model_name='segment',
            name='end_point',
            field=models.ForeignKey(default=1330, on_delete=django.db.models.deletion.PROTECT, related_name='end_point', to='roads.addresses'),
        ),
        migrations.AlterField(
            model_name='segment',
            name='start_point',
            field=models.ForeignKey(default=1330, on_delete=django.db.models.deletion.PROTECT, related_name='start_point', to='roads.addresses'),
        ),
    ]
