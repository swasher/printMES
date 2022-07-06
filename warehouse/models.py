# coding: utf-8
from django.db import models
from core.models import Customer
from stanzforms.models import Knife


class Maquette(models.Model):
    """
    This model describe a box or a label and his relation to Customer.
    """
    customer = models.ForeignKey(Customer, on_delete=models.RESTRICT)
    remote_filename = models.CharField(max_length=256) # Название файла этикетки или коробки. Абсолютный путь - os.path.join(customer.unc, filename)
    name = models.CharField(max_length=150, blank=True)
    last_change = models.DateField(blank=True, null=True, help_text='Дата-время последнего изменения исходника') # нужно ли указывать время изменения или достачто только даты?
    approved = models.BooleanField(help_text='Заказчик утвердил макет', default=False)
    approved_date = models.DateField(help_text='Дата утверждения', blank=True, null=True) # Если макет изменился со времени последнего подтверждения, что галка Approved снимается
    thumb = models.ImageField(max_length=200, blank=True, null=True) # small image for grid, about 100x100 px
    preview = models.ImageField(max_length=200, blank=True, null=True) # big image about screen width
    width = models.PositiveSmallIntegerField(blank=True, null=True, help_text='Ширина по тримбоксу, мм')
    height = models.PositiveSmallIntegerField(blank=True, null=True, help_text='Высота по тримбоксу, мм')
    is_cutting = models.BooleanField(blank=True, default=False) # Если изделие высекается, то можно связать с ним Нож
    knife = models.ForeignKey(Knife, blank=True, null=True, on_delete=models.SET_DEFAULT, default=None)  # TODO указывать на некий DELETED_KNIFE, чтобы знать, что он был, но теперь удален

    def folder(self):
        # Обычно путь примерно такой /warehouse/firm/brand/brand1/pachtet.jpg
        # Нам убрать warehouse (корневую папку хранения), firm - папку заказчика и имя файла,
        # оставивив только brand/brand1
        return '/'.join(self.thumb.name.split('/')[2:-1])


"""
Во-первых, что непонятно - это как логинится Кастомеру. Потому что Customer не наследован от User 

Второй момент, как я думаю сделать.
Форма Warehouse. Менеджер выбирает Кастомера из дроп-спикска и тут же вводит предполагаемый тираж.
Далее он напротив каждой позиции проставляет кол-во на листе и жмет Save. Эти данные сохраняются либо в
shelve, либо прямо в таблице Warehouse, и напротив каждой позиции появляется тираж. 

Далее менеджер нажимает кнопку `SAVE PDF` и сохраняет пдф с картинками, названиями изделий, кол-вом на листе и тиражом.
Ту же самую процедуру может проделать заказчик самостоятельно

Можно так-же предусмотреть кнопку APPROVED типа заказчик "подтвердил" макет. После скана, если макет изменился,
подтвердить нужно заново. На этой кнопке можно повесить JS попап для подтверждения.

MD5 или FILESIZE - как быстрее и надежнее отслеживать изменение макета? Проверка показала, что filesize меняется
при малейшем изменении макета, типа подвинуть объект на миллиметр. 

"""

