# Generated by Django 4.0.5 on 2022-07-03 14:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Paper',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=150, verbose_name='Наименование бумаги')),
                ('grammage', models.IntegerField()),
                ('type', models.CharField(blank=True, choices=[('matt', 'Matt'), ('gloss', 'Gloss'), ('uncoated', 'Uncoated'), ('kartons', 'Kartons')], max_length=8, null=True, verbose_name='Тип бумаги')),
                ('paper_warehouse_unit', models.CharField(blank=True, choices=[('leaf', 'Листы'), ('kg', 'Кг')], help_text='В каких единицах приходована бумаги (кг или листы)', max_length=4, null=True, verbose_name='Ед.:')),
                ('paper_warehouse_format', models.CharField(blank=True, help_text='Формат бумаги НА СКЛАДЕ', max_length=20, verbose_name='Формат СКЛАД')),
            ],
        ),
    ]
