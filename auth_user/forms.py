from django.contrib.auth.models import User
from vehicle.models import ScheduleMaintenance
from django import forms



class UserLoginForms(forms.Form):
  username = forms.CharField(max_length=200)
  password = forms.CharField(max_length=200)
  
  
class UserRegistrationForms(forms.ModelForm):
  class Meta:
    model = User
    fields = ['username', 'password', 'first_name', 'last_name']
    
    
  def save(self, commit=True):
    instance = super().save(commit=False)
    instance.set_password(self.cleaned_data['password'])
    print('Password ', self.cleaned_data['password'])
    if commit:
      print ('commited')
      instance.save()
    return super().save()  
  
  
  
class ScheduleForms(forms.ModelForm):
  class Meta:
    fields = ScheduleMaintenance
    fields = '__all__'
    exclude = ['created_at']