# Generated by Django 4.0.4 on 2022-05-16 16:48

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('booking', '0007_remove_menu_item_remove_restaurants_menu_id_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='orders',
            name='items',
        ),
        migrations.AddField(
            model_name='orders',
            name='complete',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='orders',
            name='customer',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='orders',
            name='date_ordered',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
        migrations.CreateModel(
            name='OrderItem',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity', models.IntegerField(blank=True, default=0, null=True)),
                ('date_added', models.DateTimeField(auto_now_add=True)),
                ('order', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='booking.orders')),
                ('product', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='booking.items')),
            ],
        ),
    ]
