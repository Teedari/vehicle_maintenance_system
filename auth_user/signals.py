from django.dispatch import receiver
from django.db.models.signals import post_save
from django.contrib.auth.models import User
from auth_user.models import Profile
from vehicle.models import Maintenance



@receiver(post_save, sender=User)
def update_new_token(sender, instance, created, **kwargs):
  if created:
    profile = Profile.objects.create(user = instance)
    profile.save()

