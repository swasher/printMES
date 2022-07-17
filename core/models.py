from django.db import models
from django.contrib.auth.models import User


class Employee(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone = models.CharField(max_length=13, blank=True)

    class Meta:
        verbose_name = 'Сотрудник'
        verbose_name_plural = 'Сотрудники'

    def __str__(self):
        return ' '.join(self.user.username)


class Customer(models.Model):
    """
    Наследуется от User, потому что Заказчик может логинится и смотреть свои файлы.
    """
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)
    name = models.CharField(max_length=150)
    address = models.CharField(max_length=250, blank=True)
    fio = models.CharField(max_length=150, blank=True, verbose_name='ФИО', help_text='ФИО и должность контактного лица')
    phone = models.CharField(max_length=50, blank=True, help_text='Телефон контактного лица')
    remarks = models.TextField(blank=True, verbose_name='Примечания')
    allow_access = models.BooleanField(blank=False, default=False) # customer allow access to their Products
    unc = models.CharField(max_length=150, blank=True, null=True) # path to source products \\Server\SharedFolder\Customer\Files

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Заказчик'
        verbose_name_plural = 'Заказчики'


class Contractor(models.Model):
    PRODUCE = (
        ('ctp', 'Формы'),
        ('kli', 'Клише'),
        ('sta', 'Штанцы'),
        ('all', 'Разное'),
    )
    name = models.CharField(max_length=100, verbose_name='Организация', unique=True)
    produce = models.CharField(blank=True, null=True, max_length=3, choices=PRODUCE, verbose_name='Производство')
    phone = models.CharField(max_length=50, blank=True, verbose_name='Телефон')
    remarks = models.TextField(blank=True, verbose_name='Примечания')

    def __str__(self):
        return u'{}'.format(self.name)

    class Meta:
        verbose_name = 'Подрядчик'
        verbose_name_plural = 'Подрядчики'


class PrintingPress(models.Model):
    name = models.CharField(max_length=150, verbose_name='Наименование', help_text='Название печатного пресса')
    plate_w = models.IntegerField(verbose_name='Ширина пластины, мм')
    plate_h = models.IntegerField(verbose_name='Высота пластины, мм')
    klapan = models.IntegerField(verbose_name='Клапан', help_text='Расстояние от нижнего края пластины до края бумаги')
    cost = models.IntegerField(blank=True, null=True, help_text='Cost of one plate')

    class Meta:
        verbose_name = 'PrintPress'
        verbose_name_plural = 'PrintPresses'

    def __str__(self):
        return self.name


class Equipment(models.Model):
    name = models.CharField(max_length=50)
    class Meta:
        verbose_name = 'Оборудование'
        verbose_name_plural = 'Оборудование'


class TechnologicalOperation(models.Model):
    """
    Мысли, как рассчитывать стоимость операций... К примеру,
    - ламинат: площадь листа * (тираж + приладка) * стоимость кв. метра материала
    -

    У каждой операции должен быть рассчитан ОТХОД в листах. Его надо просуммировать и добавить к Тиражу.
    У каждой операции должен быть список совместимого ОБОРУДОВАНИЯ

    У каждой операции должны быть РЕКВИЗИТЫ. К примеру,
    - вырубка:
        - номер штанца
    - ламинация
        - тип ламината
    - тиснение
        - цвет фольги
    - фальцовка
        - тип фальцовки (гармошка, труба, и т.д)
        - кол-во сгибов
    - склейка блока
        - сторона

    """
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Технологическая операция'
        verbose_name_plural = 'Технологические операции'


class PaperSize(models.Model):
    name = models.CharField(max_length=50)
    width = models.IntegerField(verbose_name='Ширина бумаги, мм')
    height = models.IntegerField(verbose_name='Высота бумаги, мм')
    comment = models.CharField(max_length=50, blank=True, null=True)
    is_printing = models.BooleanField(verbose_name='May print', help_text='На этом формате можно печатать')

    def __str__(self):
        return self.name


class Paper(models.Model):
    PAPER_TYPE = (
        ('matt', 'Matt'),
        ('gloss', 'Gloss'),
        ('uncoated', 'Uncoated'),
        ('kartons', 'Kartons'),
    )
    PAPER_UNIT = (
        ('leaf', 'Листы'),
        ('kg', 'Кг'),
    )
    name = models.CharField(max_length=150, verbose_name='Наименование бумаги')
    grammage = models.IntegerField()
    type = models.CharField(blank=True, null=True, max_length=8, choices=PAPER_TYPE, verbose_name='Тип бумаги')
    paper_warehouse_unit = models.CharField(blank=True, null=True, max_length=4, choices=PAPER_UNIT, verbose_name='Ед.:', help_text='В каких единицах приходована бумаги (кг или листы)')
    paper_warehouse_format = models.ForeignKey(PaperSize, verbose_name='Формат СКЛАД', help_text='Формат бумаги НА СКЛАДЕ', on_delete=models.RESTRICT)
    description = models.TextField()

    def __str__(self):
        return ' '.join([self.name, str(self.grammage)])
