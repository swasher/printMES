# Generated by Django 4.0.6 on 2022-07-23 11:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='ordermagazine',
            name='order_ptr',
        ),
        migrations.RemoveField(
            model_name='ordermontage',
            name='order_ptr',
        ),
        migrations.RemoveField(
            model_name='orderpack',
            name='order_ptr',
        ),
        migrations.AlterModelOptions(
            name='operation',
            options={'ordering': ['operation_sequence'], 'verbose_name': 'Операция', 'verbose_name_plural': 'Операции'},
        ),
        migrations.AddField(
            model_name='operation',
            name='operation_sequence',
            field=models.PositiveIntegerField(db_index=True, default=0, help_text='Поле для плагина sortable2 чтобы упорядочивать операции'),
        ),
        migrations.DeleteModel(
            name='OrdedNonStandart',
        ),
        migrations.DeleteModel(
            name='OrderMagazine',
        ),
        migrations.DeleteModel(
            name='OrderMontage',
        ),
        migrations.DeleteModel(
            name='OrderPack',
        ),
    ]