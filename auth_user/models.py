from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Profile(models.Model):
  user = models.ForeignKey(to=User, related_name='user', blank=True, null=True, on_delete=models.CASCADE)
  
  def __str__(self):
    return self.user