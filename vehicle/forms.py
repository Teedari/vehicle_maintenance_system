import json
from django import forms
from django.db.models import fields
from .models import Customer, Vehicle, Service

class VehicleRegistrationForm(forms.ModelForm):
  class Meta:
    model = Vehicle
    fields = '__all__'
    
class CustomRegisterationForm(forms.ModelForm):
  class Meta:
    model = Customer
    fields = '__all__'
    exclude = ['vehicles']
    
class ServiceForm(forms.ModelForm):
  class Meta:
    model = Service
    exclude = ['created_at']
    
    
  def save(self, commit=True):
    data  = super().save(commit = False)
    print('Save-Method: ', data)
    if commit:
      data.save()
     
    return data