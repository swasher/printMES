# coding: utf-8

from django.db import models
# from django.db.models import Max
from django.contrib.auth.models import User
from core.models import PrintingPress
from core.models import Customer
from core.models import Contractor
from core.models import Paper


class Order(models.Model):
    is_production = models.BooleanField(default=False, help_text='Заказ находится в производстве')
    order = models.IntegerField(unique=True, verbose_name='Номер заказа', help_text='Max order')
    customer = models.ForeignKey(Customer, verbose_name='Заказчик', on_delete=models.RESTRICT)
    name = models.CharField(max_length=100, verbose_name='Наименование заказа')
    quantity = models.IntegerField(verbose_name='Тираж', help_text='Общее кол-во заказанных изделий')
    price = models.DecimalField(max_digits=12, decimal_places=2, blank=True, null=True, verbose_name='Стоимость, грн.')
    start_date = models.DateField(verbose_name='Дата оформления', help_text='Дата оформления заказа')
    end_date = models.DateField(blank=True, null=True, verbose_name='Сдать до', help_text='Предполагаемая дата сдачи заказа')
    remarks = models.TextField(blank=True, verbose_name='Описание заказа')
    status_ready = models.BooleanField(default=False, help_text='True когда заказ готов к выдаче заказчику.')
    status_ready_user = models.ForeignKey(User, blank=True, null=True, on_delete=models.RESTRICT)

    class Meta:
        verbose_name = 'Заказ'
        verbose_name_plural = 'Заказы'

    def calc_field(self):
        try:
            unit_price = '{:.2f}'.format(self.price / self.quantity)
        except TypeError:
            unit_price = '0'
        return unit_price
    calc_field.short_description = 'unit_price'

    def __str__(self):
        return 'Заказ {} от {} [{}]'.format(self.name, self.customer.name, self.quantity)


class PrintSheet(models.Model):
    TURNOVER = (
        ('SingleSide', 'Без оборота'),
        ('WorkAndTurn', 'Свой оборот'),
        ('WorkAndThumble', 'Хвост-на-голову'),
        ('Perfecting', 'Чужой оборот'),
    )
    name = models.CharField(max_length=150, null=False, verbose_name='Название листа')
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    printingpress = models.ForeignKey(PrintingPress, blank=True, null=True, verbose_name='Печатная машина', on_delete=models.RESTRICT)
    pressrun = models.IntegerField(blank=True, null=True, verbose_name='Тираж', help_text='Технологический тираж одного листа')
    plates = models.PositiveSmallIntegerField(blank=True, null=True, verbose_name='Пластины', help_text='Кол-во пластин на один лист')
    color_front = models.CharField(max_length=10, blank=True, null=False, verbose_name='F', help_text='Кол-во красок на лице')
    color_back = models.CharField(max_length=10, blank=True, null=False, verbose_name='B', help_text='Кол-во красок на обороте, 0 - если без оборота')
    quantity = models.PositiveSmallIntegerField(blank=True, null=True, verbose_name='Листов', help_text='Кол-во одинаковых печатных листов')
    turnover = models.CharField(blank=True, null=True, max_length=20, choices=TURNOVER, verbose_name='Оборот')
    paper = models.ForeignKey(Paper, blank=True, null=True, max_length=300, verbose_name='Граммаж и тип бумаги', on_delete=models.RESTRICT)
    paper_printing_amount = models.CharField(max_length=20, blank=True, verbose_name='Кол-во листов', help_text='Необходимо выдать листов со склада')
    paper_printing_format = models.CharField(max_length=20, blank=True, verbose_name='Формат печати', help_text='Формат бумаги в печать')

    class Meta:
        verbose_name = 'Печатный лист'
        verbose_name_plural = 'Печатные листы'

    def __str__(self):
        return '{} [{} {}]'.format(self.name, self.printingpress, '+'.join([self.color_front, self.color_back]))


class OperationList(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Словарь технологических операций'
        verbose_name_plural = 'Словарь технологических операций'


class Operation(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    name = models.ForeignKey(OperationList, verbose_name='Операция', help_text='', on_delete=models.CASCADE)
    printsheet = models.ForeignKey(PrintSheet, blank=True, null=True, verbose_name='Печатный лист', help_text='Если оперция не относится к конкретному печатному листу, оставьте это поле пустым', on_delete=models.CASCADE)
    contractor = models.ForeignKey(Contractor, blank=True, null=True, verbose_name='Подрядчик', on_delete=models.RESTRICT)
    price = models.DecimalField(max_digits=12, decimal_places=2, blank=True, null=True, verbose_name='Стоимость, грн.')
    remarks = models.CharField(max_length=500, blank=True)

    class Meta:
        verbose_name = 'Операция'
        verbose_name_plural = 'Операции'

    def __str__(self):
        return self.name.name


class Detal(models.Model):
    printsheet = models.ForeignKey(PrintSheet, on_delete=models.CASCADE)
    name = models.CharField(max_length=50, verbose_name='Название детали')
    size = models.CharField(max_length=20, blank=True, null=False, verbose_name='Размер, мм')
    amount = models.PositiveIntegerField(blank=True, null=True, verbose_name='Тираж')

    class Meta:
        verbose_name = 'Деталь'
        verbose_name_plural = 'Детали'

    def __str__(self):
        if self.size:
            return '{} [{}]'.format(self.name, self.size)
        else:
            return self.name