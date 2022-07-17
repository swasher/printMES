# Generated by Django 4.0.6 on 2022-07-16 06:42

from django.db import migrations, models
import django.db.models.deletion
import stanzforms.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('core', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Doska',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('articul', models.CharField(max_length=20, unique=True, verbose_name='Артикул')),
                ('make_date', models.DateField(blank=True, null=True, verbose_name='Дата изг.')),
                ('name', models.CharField(max_length=100, verbose_name='Наименование')),
                ('price', models.DecimalField(blank=True, decimal_places=2, max_digits=12, null=True, verbose_name='Стоимость, уе.')),
                ('description', models.TextField(blank=True, verbose_name='Описание')),
                ('maintenance', models.TextField(blank=True, help_text='Тут должны быть описаны любые работы, проведенные с доской.', verbose_name='Обслуживание')),
                ('customer', models.TextField(blank=True, help_text='Кто платил, или типичные заказчики.', verbose_name='Заказчик')),
                ('spusk', models.ImageField(blank=True, help_text='Изображение печатного листа', null=True, upload_to=stanzforms.models.get_spusk_file_path, verbose_name='Спуск')),
                ('doska', models.ImageField(blank=True, help_text='Изображение доски', null=True, upload_to=stanzforms.models.get_doska_file_path, verbose_name='Доска')),
                ('contractor', models.ForeignKey(on_delete=django.db.models.deletion.RESTRICT, to='core.contractor', verbose_name='Изготовитель')),
            ],
            options={
                'verbose_name': 'Доска',
                'verbose_name_plural': 'Доски',
            },
        ),
        migrations.CreateModel(
            name='Knife',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('razvertka_w', models.PositiveSmallIntegerField(blank=True, help_text='Развертка, ширина', null=True)),
                ('razvertka_h', models.PositiveSmallIntegerField(blank=True, help_text='Развертка, высота', null=True)),
                ('gabarit_a', models.PositiveSmallIntegerField(blank=True, help_text='Габарит ширина', null=True)),
                ('gabarit_b', models.PositiveSmallIntegerField(blank=True, help_text='Габарит высота', null=True)),
                ('gabarit_c', models.PositiveSmallIntegerField(blank=True, help_text='Габарит глубина', null=True)),
                ('knife', models.ImageField(blank=True, help_text='Изображение ножа', null=True, upload_to=stanzforms.models.get_knife_file_path, verbose_name='Нож, изобр.')),
                ('drawing', models.FileField(blank=True, help_text='Файл чертежа (PDF)', null=True, upload_to=stanzforms.models.get_drawing_file_path, verbose_name='Чертеж, PDF')),
                ('doska', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='stanzforms.doska')),
            ],
            options={
                'verbose_name': 'Штанц',
                'verbose_name_plural': 'Штанцы',
            },
        ),
    ]