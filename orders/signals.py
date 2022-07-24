from django.db.models.signals import post_save
from django.dispatch import receiver

from orders.models import Order
from orders.models import PrintSheet



@receiver(post_save, sender=PrintSheet)
def renaming_press_sheets(sender, instance, **kwargs):
    """
    Автонумерация печатных листов
    """
    # If instance/row is being created, then do nothing
    if instance.id is None:
        pass

    print("Signal RUNNING! Instance=", instance)
    print("Order #", instance.order.order)
    q = PrintSheet.objects.filter(order__pk=instance.order.pk)
    curr_list = 0
    for i in q:
        print(i, '-----', i.same_sheets, 'curr is', curr_list)
        if i.same_sheets == 1:
            name = 'List' + str(curr_list+1)
        else:
            name = 'List' + str(curr_list + 1) + '-' + str(curr_list + i.same_sheets)
        curr_list += i.same_sheets
        PrintSheet.objects.filter(pk=i.pk).update(name=name)
