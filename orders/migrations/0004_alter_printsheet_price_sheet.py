# Generated by Django 4.0.6 on 2022-07-16 11:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0003_alter_printsheet_paper_printing_amount'),
    ]

    operations = [
        migrations.AlterField(
            model_name='printsheet',
            name='price_sheet',
            field=models.FloatField(blank=True, help_text='Стоимость печати', null=True, verbose_name='Price'),
        ),
    ]