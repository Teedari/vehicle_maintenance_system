from django.db import models

# Create your models here.

VEHICLE_TYPES = (
  ('toyota', 'Toyota'),
  ('nissan', 'Nissan'),
  ('vibe', 'Vibe'),
  ('v8', 'V8'),
  ('mercedes-benz', 'Mercedes-benz'),
  ('rolls', 'Rolls'),
  ('rolls royce', 'Rolls Royce'),
)
class Vehicle(models.Model):
  id = models.AutoField(primary_key=True)
  vehicle_year = models.CharField(max_length=4, blank=True)
  vehicle_type = models.CharField(choices=(VEHICLE_TYPES), max_length=15)
  vehicle_make = models.CharField(max_length=100,)
  vehicle_model = models.CharField(max_length=100,)
  vehicle_number_plate = models.CharField(max_length=100, blank=True)
  
  def __str__(self):
    return '{} {} {}'.format(self.vehicle_year, self.vehicle_make, self.vehicle_number_plate)
  
  
class Customer(models.Model):
  id = models.AutoField(primary_key=True)
  fullname = models.CharField(max_length=200)
  phone = models.CharField(max_length=10)
  email = models.EmailField(max_length=100, blank=True)
  address = models.TextField(default='no address provided', blank=True)
  vehicles = models.ManyToManyField(Vehicle, related_name='vehicles' , blank=True)
  created_at = models.DateTimeField(auto_now_add=True)
  

  def __str__(self):
    return '{} - {}'.format(self.fullname, self.created_at)
  
  @property
  def get_initials(self):
    name = self.fullname
    first_name_initial = self.fullname[0].upper()
    last_name_index = [i for i in range(len(name)) if name[i] == ' '][0] + 1
    last_name_initial = name[last_name_index]
    initials = '{}{}'.format(first_name_initial, last_name_initial)
    return initials
  
  @property
  def get_vehicle(self):
    vec =  [v for v in self.vehicles.all()]
    return 'None' if vec == [] else vec[0]
  
  
class Service(models.Model):
  id = models.AutoField(primary_key=True)
  text = models.CharField(max_length=100)
  cost = models.DecimalField(max_digits=10, decimal_places=2)
  created_at = models.DateTimeField(auto_now_add=True)
  
  def __str__(self):
    return '{} - {}'.format(self.text, self.cost)
  
  
class Maintenance(models.Model):
  id = models.AutoField(primary_key=True)
  owner = models.ForeignKey(to=Customer, related_name='user', on_delete=models.CASCADE)
  service = models.ForeignKey(to=Service, on_delete=models.CASCADE, blank=True, related_name='service')
  token = models.CharField(max_length=200, blank=True)
  created_at = models.DateTimeField(auto_now_add=True)
  
  def __str__(self):
    return '{} - T:{}'.format(self.id, self.token)
  
  
  @property
  def customer(self):
    return self.owner.fullname
  
  @property
  def contact(self):
    return self.owner.phone
  
  @property
  def vehicle(self):
    return self.owner.get_vehicle
  
  @property
  def vehicle_type(self):
    return self.owner.get_vehicle.vehicle_type
  
  @property
  def service_detail(self):
    return self.service.text

  @property
  def amount(self):
    return self.service.cost
  
  
  
  
  
class ScheduleMaintenance(models.Model):
  customer = models.OneToOneField(to=Customer, on_delete=models.CASCADE, primary_key=True, unique=True)
  date = models.DateField(auto_now_add=True)
  created_at = models.DateTimeField(auto_now=True)