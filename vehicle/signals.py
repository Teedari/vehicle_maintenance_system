from django.dispatch import receiver
from django.db.models.signals import post_save

from vehicle.models import Maintenance



# @receiver(post_save, sender=Maintenance)
# def update_new_token(sender, instance, created, **kwargs):
#   if created:
#     _instance = instance
#     _instance.token = 'TOKEN-{}'.format(instance.id)
#     _instance.save()

