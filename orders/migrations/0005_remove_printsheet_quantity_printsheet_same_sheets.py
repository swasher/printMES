# Generated by Django 4.0.6 on 2022-07-16 18:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0004_alter_printsheet_price_sheet'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='printsheet',
            name='quantity',
        ),
        migrations.AddField(
            model_name='printsheet',
            name='same_sheets',
            field=models.PositiveSmallIntegerField(blank=True, help_text='Кол-во одинаковых печатных листов', null=True, verbose_name='Одинаковых'),
        ),
    ]