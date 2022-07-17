# Generated by Django 4.0.6 on 2022-07-16 06:42

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Contractor',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, unique=True, verbose_name='Организация')),
                ('produce', models.CharField(blank=True, choices=[('ctp', 'Формы'), ('kli', 'Клише'), ('sta', 'Штанцы'), ('all', 'Разное')], max_length=3, null=True, verbose_name='Производство')),
                ('phone', models.CharField(blank=True, max_length=50, verbose_name='Телефон')),
                ('remarks', models.TextField(blank=True, verbose_name='Примечания')),
            ],
            options={
                'verbose_name': 'Подрядчик',
                'verbose_name_plural': 'Подрядчики',
            },
        ),
        migrations.CreateModel(
            name='Equipment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
            ],
            options={
                'verbose_name': 'Оборудование',
                'verbose_name_plural': 'Оборудование',
            },
        ),
        migrations.CreateModel(
            name='PaperSize',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('width', models.IntegerField(verbose_name='Ширина бумаги, мм')),
                ('height', models.IntegerField(verbose_name='Высота бумаги, мм')),
                ('comment', models.CharField(blank=True, max_length=50, null=True)),
                ('is_printing', models.BooleanField(help_text='На этом формате можно печатать', verbose_name='May print')),
            ],
        ),
        migrations.CreateModel(
            name='PrintingPress',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(help_text='Название печатного пресса', max_length=150, verbose_name='Наименование')),
                ('plate_w', models.IntegerField(verbose_name='Ширина пластины, мм')),
                ('plate_h', models.IntegerField(verbose_name='Высота пластины, мм')),
                ('klapan', models.IntegerField(help_text='Расстояние от нижнего края пластины до края бумаги', verbose_name='Клапан')),
                ('cost', models.IntegerField(blank=True, help_text='Cost of one plate', null=True)),
            ],
            options={
                'verbose_name': 'PrintPress',
                'verbose_name_plural': 'PrintPresses',
            },
        ),
        migrations.CreateModel(
            name='TechnologicalOperation',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
            ],
            options={
                'verbose_name': 'Технологическая операция',
                'verbose_name_plural': 'Технологические операции',
            },
        ),
        migrations.CreateModel(
            name='Paper',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=150, verbose_name='Наименование бумаги')),
                ('grammage', models.IntegerField()),
                ('type', models.CharField(blank=True, choices=[('matt', 'Matt'), ('gloss', 'Gloss'), ('uncoated', 'Uncoated'), ('kartons', 'Kartons')], max_length=8, null=True, verbose_name='Тип бумаги')),
                ('paper_warehouse_unit', models.CharField(blank=True, choices=[('leaf', 'Листы'), ('kg', 'Кг')], help_text='В каких единицах приходована бумаги (кг или листы)', max_length=4, null=True, verbose_name='Ед.:')),
                ('paper_warehouse_format', models.ForeignKey(help_text='Формат бумаги НА СКЛАДЕ', on_delete=django.db.models.deletion.RESTRICT, to='core.papersize', verbose_name='Формат СКЛАД')),
            ],
        ),
        migrations.CreateModel(
            name='Employee',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('phone', models.CharField(blank=True, max_length=13)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Сотрудник',
                'verbose_name_plural': 'Сотрудники',
            },
        ),
        migrations.CreateModel(
            name='Customer',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=150)),
                ('address', models.CharField(blank=True, max_length=250)),
                ('fio', models.CharField(blank=True, help_text='ФИО и должность контактного лица', max_length=150, verbose_name='ФИО')),
                ('phone', models.CharField(blank=True, help_text='Телефон контактного лица', max_length=50)),
                ('remarks', models.TextField(blank=True, verbose_name='Примечания')),
                ('allow_access', models.BooleanField(default=False)),
                ('unc', models.CharField(blank=True, max_length=150, null=True)),
                ('user', models.OneToOneField(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Заказчик',
                'verbose_name_plural': 'Заказчики',
            },
        ),
    ]
