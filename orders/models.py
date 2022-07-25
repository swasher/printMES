# coding: utf-8

from django.db import models
# from django.db.models import Max
from django.contrib.auth.models import User
from core.models import PrintingPress
from core.models import Customer
from core.models import Contractor
from core.models import Paper
from core.models import Employee
from core.models import TechnologicalOperation

"""
Мысли, что можно сделать 
- адрес доставки (поле контрагента)
- адрес выставления счета (поле контрагента)
- статус платежа
- частичная отгрузка
- статус 'draft' (предв. расчет) у заказа, к примеру, такой заказ не будет виден другим менеждарам...
"""

class Order(models.Model):
    TYPE = (
        ('det', 'Детали'),
        ('pol', 'Полосы'),
    )
    is_production = models.BooleanField(default=False, help_text='Заказ находится в производстве')
    order = models.IntegerField(unique=True, verbose_name='Номер заказа', help_text='Max order')
    manager = models.ForeignKey(Employee, verbose_name='Менеджер', on_delete=models.RESTRICT)
    customer = models.ForeignKey(Customer, verbose_name='Заказчик', on_delete=models.RESTRICT)
    name = models.CharField(max_length=100, verbose_name='Наименование заказа')
    quantity = models.IntegerField(verbose_name='Тираж', help_text='Общее кол-во заказанных изделий')
    price = models.DecimalField(max_digits=12, decimal_places=2, blank=True, null=True, verbose_name='Стоимость, eur.')
    start_date = models.DateField(verbose_name='Дата оформления', help_text='Дата оформления заказа')
    end_date = models.DateField(blank=True, null=True, verbose_name='Сдать до', help_text='Предполагаемая дата сдачи заказа')
    remarks = models.TextField(blank=True, verbose_name='Описание заказа')
    status_ready = models.BooleanField(default=False, help_text='True когда заказ готов к выдаче заказчику.')
    type = models.CharField(max_length=3, choices=TYPE, verbose_name='Тип заказа')

    class Meta:
        verbose_name = 'Заказ'
        verbose_name_plural = 'Заказы'

    def unit_price_calculated(self):
        try:
            unit_price = '{:.2f}'.format(self.price / self.quantity)
        except TypeError:
            unit_price = '0'
        return unit_price
    unit_price_calculated.short_description = 'unit_price'

    def __str__(self):
        return 'Заказ {} от {} [{}gb.]'.format(self.name, self.customer.organization, self.quantity)


"""
TODO
Возможно, имеет смысл сделать несколько моделей Заказов:
- для монтажной продукции (содержит Детали)
- для упаковки - по идее, то же самое что и Монтаж
- сборный и нестандартный спуск - оформляется просто как Печатные Листы вручную, по сути то же самое что и Монтаж 
- для книжно-журнальной продукции (содержит не Детали, а Полосы)

Получается, что отличается только заказ с Полосами вместо Деталей.

С другой стороны, модель может не меняться, потому что различие состоит в том, что ДРУГИЕ модели ссылаются
на эту, то есть если монтаж - то мы имеем записи Detal, ссылающиеся на Order, если Package, то Stanzforms ссылающиеся 
на Order... но тогда нужно продумать разницу в интерфейсе... различен и ввод заказа, и его отображение...

class OrderPack(Order):
    pass
class OrderMagazine(Order):
    pass
class OrderMontage(Order):
    pass
class OrdedNonStandart(Order):
    pass

"""

class PrintSheet(models.Model):
    TURNOVER = (
        ('SingleSide', 'Без оборота'),
        ('WorkAndTurn', 'Свой оборот'),
        ('WorkAndThumble', 'Хвост-на-голову'),
        ('Perfecting', 'Чужой оборот'),
    )
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    name = models.CharField(max_length=150, null=False, verbose_name='Название листа')
    description = models.CharField(max_length=150, null=True, blank=True, verbose_name='Описание листа')
    printingpress = models.ForeignKey(PrintingPress, blank=True, null=True, verbose_name='Печатная машина', on_delete=models.RESTRICT)
    pressrun = models.IntegerField(blank=True, null=True, verbose_name='Тираж', help_text='Технологический тираж одного листа')
    plates = models.PositiveSmallIntegerField(blank=True, null=True, verbose_name='Пластины', help_text='Кол-во пластин на один лист')
    color_front = models.CharField(max_length=10, blank=True, null=False, verbose_name='F', help_text='Кол-во красок на лице')
    color_back = models.CharField(max_length=10, blank=True, null=False, verbose_name='B', help_text='Кол-во красок на обороте, 0 - если без оборота')
    same_sheets = models.PositiveSmallIntegerField(blank=False, default=1, verbose_name='Одинаковых', help_text='Кол-во одинаковых печатных листов')
    turnover = models.CharField(blank=True, null=True, max_length=20, choices=TURNOVER, verbose_name='Оборот')
    paper = models.ForeignKey(Paper, blank=True, null=True, max_length=300, verbose_name='Граммаж и тип бумаги', on_delete=models.RESTRICT)
    paper_printing_amount = models.IntegerField(blank=True, null=True, verbose_name='Кол-во листов', help_text='Необходимо выдать листов со склада')
    paper_printing_format = models.CharField(max_length=20, blank=True, verbose_name='Формат печати', help_text='Формат бумаги в печать')
    price_sheet = models.FloatField(blank=True, null=True, verbose_name='Price', help_text='Стоимость печати')
    printsheet_sequence = models.PositiveIntegerField(default=0, blank=False, null=False, db_index=True, help_text='Поле для плагина sortable2 чтобы упорядочивать листы')

    class Meta:
        verbose_name = 'Печатный лист'
        verbose_name_plural = 'Печатные листы'
        ordering = ['printsheet_sequence']

    def __str__(self):
        return '{} [{} {}]'.format(self.name, self.printingpress, '+'.join([self.color_front, self.color_back]))

    def calculate_price_printsheet(self):
        try:
            sum = self.paper_printing_amount * 10
        except:
            sum = None
        return sum

    def save(self, *args, **kwargs):
        self.price_sheet = self.calculate_price_printsheet()
        super(PrintSheet, self).save(*args, **kwargs)


class Detal(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    printsheet = models.ForeignKey(PrintSheet, blank=True, null=True, on_delete=models.CASCADE)
    name = models.CharField(max_length=50, verbose_name='Название детали')
    width = models.IntegerField(verbose_name='Высота', blank=True, null=True, help_text='Размер детали, высота, мм')
    height = models.IntegerField(verbose_name='Ширина', blank=True, null=True, help_text='Размер детали, ширина, мм')
    amount = models.PositiveIntegerField(blank=True, null=True, verbose_name='Тираж')

    class Meta:
        verbose_name = 'Деталь'
        verbose_name_plural = 'Детали'

    def __str__(self):
        if self.width and self.height:
            return '{} [{}x{}]'.format(self.name, self.width, self.height)
        else:
            return self.name


"""
Можно ввести понятие ТЕТРАДЬ...
Тогда ИЗДЕЛИЕ типа книжно-журнальное будет состоять из ТЕТРАДЕЙ... 
Можно сделать базу тетрадей.. Основеное св-во Тетради - кол-во страниц.. из него вычисляется, сколько тетрадей в изделии...
"""


class Operation(models.Model):
    """
    Операции, по идее, не могут выполняться над деталями... Ну сложно себе предстваить, хотя и возможно...
    Например, две коробки на листе, одна ламинируется, другая нет...
    А как быть, если к примеру у журнала на лице есть Тиснение?...
    """
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    name = models.ForeignKey(TechnologicalOperation, verbose_name='Операция', help_text='', on_delete=models.CASCADE)
    printsheet = models.ForeignKey(PrintSheet, blank=True, null=True, verbose_name='Печатный лист', help_text='Если оперция не относится к конкретному печатному листу, оставьте это поле пустым', on_delete=models.CASCADE)
    contractor = models.ForeignKey(Contractor, blank=True, null=True, verbose_name='Подрядчик', on_delete=models.RESTRICT)
    price = models.DecimalField(max_digits=12, decimal_places=2, blank=True, null=True, verbose_name='Стоимость, EUR.')
    remarks = models.CharField(max_length=500, blank=True)
    operation_sequence = models.PositiveIntegerField(default=0, blank=False, null=False, db_index=True, help_text='Поле для плагина sortable2 чтобы упорядочивать операции')

    class Meta:
        verbose_name = 'Операция'
        verbose_name_plural = 'Операции'
        ordering = ['operation_sequence']

    def __str__(self):
        return self.name.name
