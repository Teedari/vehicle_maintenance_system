from django.test import TestCase
from .models import *
import datetime
# Create your tests here.

class VehicleTestCase(TestCase):
  
  @classmethod
  def setUp(cls):
    customer = Customer(fullname='John Doe', phone='0247440223', email='john@gmail.com')
    customer.save()
    
    
    vehicle = Vehicle(vehicle_year='2021', vehicle_type=VEHICLE_TYPES[2][1],vehicle_make='make', vehicle_model='C20',vehicle_number_plate='UE20032717')
    vehicle.save()
    
    vehicle = Vehicle(vehicle_year='2021', vehicle_type=VEHICLE_TYPES[2][1],vehicle_make='make', vehicle_model='C100',vehicle_number_plate='UE20032617')
    vehicle.save()

  def testCreateCustomer(self):

    ##testing
    test_customer = Customer.objects.get(fullname='John Doe')
    self.assertEqual(test_customer.fullname, 'John Doe')
    self.assertEqual(test_customer.phone, '0247440223')
    self.assertEqual(test_customer.email, 'john@gmail.com')
    
  def testRegisterVehicle(self):

    test_vehicle = Vehicle.objects.filter(vehicle_year = '2021')[0]
    print(test_vehicle.vehicle_type)
    self.assertEqual(test_vehicle.vehicle_make, 'make')
    
  def testVehicleToCustomer(self):
    v1 = Vehicle.objects.get(vehicle_model='C20')
    v2 = Vehicle.objects.get(vehicle_model='C100')
    customer = Customer.objects.create(fullname='TestUser', email='test@gmail.com',phone='02222222')
    customer.vehicles.add(v1, v2)
    customer.save()
    
    testCustomer = Customer.objects.get(fullname='TestUser')
    self.assertEqual(len(testCustomer.vehicles.all()) > 0 , True)
    
    
    
  
  def test_customer_initial(self):
    name = 'Godfred Dari'
    first_name_initial = name[0].upper()
    last_name_index = [i for i in range(len(name)) if name[i] == ' '][0] + 1
    last_name_initial = name[last_name_index]
    initials = '{}{}'.format(first_name_initial, last_name_initial)
    
    self.assertEqual(initials, 'GD')