from vehicle.models import ScheduleMaintenance
from django import forms



class UserLoginForms(forms.Form):
  username = forms.CharField(max_length=200)
  password = forms.CharField(max_length=200)
  
  
  
  
class ScheduleForms(forms.ModelForm):
  class Meta:
    fields = ScheduleMaintenance
    fields = '__all__'
    exclude = ['created_at']