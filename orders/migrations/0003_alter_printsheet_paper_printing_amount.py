# Generated by Django 4.0.6 on 2022-07-16 11:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0002_printsheet_description_alter_order_price'),
    ]

    operations = [
        migrations.AlterField(
            model_name='printsheet',
            name='paper_printing_amount',
            field=models.IntegerField(blank=True, help_text='Необходимо выдать листов со склада', null=True, verbose_name='Кол-во листов'),
        ),
    ]
