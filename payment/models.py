from django.db import models
import secrets
# Create your models here.

class Payment(models.Model):
  amount = models.PositiveIntegerField()
  ref = models.CharField(max_length=200)
  email = models.EmailField()
  verified = models.BooleanField(default=False) 
  created_at = models.DateTimeField(auto_now_add=True)
  
  
  class Meta:
    ordering = ('-created_at',)
    
  def __str__(self):
    return f'Payment: {self.amount}'
  
  
  def save(self, *args, **kwargs):
      while not self.ref:
        ref = secrets.token_urlsafe(50)
        validate_if_ref_exist = Payment.objects.filter(ref = ref)
        
        if not validate_if_ref_exist.exists():
          self.ref = ref
          
          
      super().save(*args, **kwargs)
      
### helper function
  @property
  def amount_value(self) -> int:
    return self.amount * 100