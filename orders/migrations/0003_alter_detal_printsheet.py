# Generated by Django 4.0.6 on 2022-07-23 12:23

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0002_remove_ordermagazine_order_ptr_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='detal',
            name='printsheet',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='orders.printsheet'),
        ),
    ]