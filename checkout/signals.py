from django.db.models.signals import post_save, post_delete #This implies these signals are sent by django to the entire application after a model instance is saved and after it's deleted respectively.
from django.dispatch import receiver # To receive these signals we can import receiver from django.dispatch.

from .models import OrderLineItem # Of course since we'll be listening for signals from the OrderLineItem model we'll also need that.

@receiver(post_save, sender=OrderLineItem)
def update_on_save(sender, instance, created, **kwargs): # function which will handle signals from the post_save event. sender = OrderLineItem instance, created,
    """
    Update order total on lineitem update/create 
    """
    instance.order.update_total()

@receiver(post_delete, sender=OrderLineItem)
def update_on_delete(sender, instance, **kwargs): 
    """
    Update order total on lineitem delete
    """
    print('delete signal recieved!')
    instance.order.update_total()