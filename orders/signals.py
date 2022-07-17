from django.db.models.signals import post_save
from django.dispatch import receiver

from orders.models import Order



@receiver(post_save, sender=Order)
def renaming_press_sheets(sender, instance, **kwargs):
    print("Signal RUNNING!")
    # instance.save()
