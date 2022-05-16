# Generated by Django 4.0.4 on 2022-05-16 08:34

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('booking', '0006_alter_bookings_phone'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='menu',
            name='item',
        ),
        migrations.RemoveField(
            model_name='restaurants',
            name='menu_id',
        ),
        migrations.AddField(
            model_name='items',
            name='menu',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to='booking.menu'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='menu',
            name='restaurant',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to='booking.restaurants'),
            preserve_default=False,
        ),
    ]
