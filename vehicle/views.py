from auth_user.forms import UserRegistrationForms
from vehicle.decorators import get_request_vehicle
from vehicle.utils import remove_duplicates
from helpers.funcs import serviceTokenGenerator
import json
from django.http import response
from vehicle.models import Customer, Maintenance, ScheduleMaintenance, Service, Vehicle
from django.shortcuts import get_object_or_404, render, Http404, reverse
from django.http import JsonResponse
from django.http.response import HttpResponse, HttpResponseRedirect
from .forms import CustomRegisterationForm, VehicleRegistrationForm, ServiceForm
from django.contrib.auth.decorators import login_required

# Create your views here.

@login_required(login_url='auth/login')
def home(request):
  _number_of_customers = Customer.objects.all().count()
  
  _number_of_services = Service.objects.all().count()
 
  _number_of_vehicles = Vehicle.objects.all().count()
  
  _number_of_total_maintenance = Maintenance.objects.all().count()
  
  _schedule_maintenance = ScheduleMaintenance.objects.all()
  
  
  
  
  context = {
    'data': {
      'customers': _number_of_customers,
      'services': _number_of_services,
      'vehicles': _number_of_vehicles,
      'maintenance': _number_of_total_maintenance,
      'scheduled_maintenance': _schedule_maintenance
    }
  }
  
  return render(request, 'vehicle/index.html', context)



def create_new_user(request):
  context = {}
  context['form'] = UserRegistrationForms()
  
  if request.method == 'POST':
    form = UserRegistrationForms(request.POST)
    if form.is_valid():
      res = form.save()
      print(res)
      
  return render(request, 'vehicle/create_user.html', context)


@login_required(login_url='auth/login')
def vehicle_register(request):
  
  try:
    request.session['count'] = 2
    
  except:
    request.session['count']  = 1
  
  
  vehicle_form = VehicleRegistrationForm()
  customer_form = CustomRegisterationForm();
  context = {
    'vehicle_form': vehicle_form,
    'customer_form': customer_form
  }
  
  
  if request.method == 'POST' and request.is_ajax():
    response = {}
    CUSTOMER_UNIQUE_ATTR = 'fullname'
    form_type = 'customer_form' if  CUSTOMER_UNIQUE_ATTR in request.POST.keys() else 'vehicle_form'
    
    
    if form_type == 'customer_form':
      _customer = CustomRegisterationForm(request.POST)
      if _customer.is_valid():
        c = _customer.save()
        request.session['customer'] = c.id
        
        request.session['count'] = 2
        
        response = {
          'status': 'success',
          'status_code': 201,
          'data': {
          'customerVNumPlate': c.id,
          'customerName': c.fullname  
          },
          
        }
        return JsonResponse(response)
    
      else:
        print('Customer Error: ', _customer.errors.as_json)
        return JsonResponse({'data': [], 'status': 'error', 'status_code': 404})
    
    if form_type is not customer_form:
      _vehicle = VehicleRegistrationForm(request.POST)
      if _vehicle.is_valid():
        
        ## save vehicle 
        v = _vehicle.save()
        request.session['customerVNumPlate'] = v.vehicle_number_plate
        ## add to customer
        _customer = Customer.objects.get(id = request.session['customer'])
        _customer.vehicles.add(v)
        _customer.save()
        
        ## sessions
        # del request.session['customer']
        request.session['count'] = 1

        response = {
          'status': 'success',
          'status_code': 201,
          'data': v.vehicle_make
        }
        return JsonResponse(response)
        # return HttpResponseRedirect(reverse('vehicle:register_render_service'))
      # print('Vehicle Error: ', _vehicle.errors.as_json)
      return JsonResponse({'data': [], 'status': 'error', 'status_code': 404})

  
  
  return render(request, 'vehicle/register_vehicle.html', context)

@login_required(login_url='auth/login')
@get_request_vehicle
def service(request):
  context = {}
  form = ServiceForm();

  services =  Service.objects.all()
  context['services'] = services
  context['form'] = form
  
  if request.method == 'GET' and request.is_ajax():
    
    res = {"status": 'success', 'data': list(services.values())}
    return JsonResponse(res)
  
  
  if request.method == 'POST':
    form = ServiceForm(data=request.POST);
    if form.is_valid():
      form.save()
      
      
      response = {
        'status': 'success',
        'data': {
          "text": form.cleaned_data.get('text'),
          "amount": form.cleaned_data.get('cost'),
          },
      }
      return JsonResponse(response)
    else:
      return JsonResponse({'message': 'Data was not saved successfully', 'errors' : form.non_form_error})

  return render(request, 'vehicle/services.html', context)



@login_required(login_url='auth/login')
def list_all_customers(request):
  qs = Customer.objects.all()
  context = {
    'customers': qs
  }
  return render(request, 'vehicle/list_customers.html', context)

@login_required(login_url='auth/login')
def list_all_services_rendered(request):
  
  context = { }
  qs = Maintenance.objects.all()
  qs = remove_duplicates(qs)
  if request.method == 'POST':
  
    qs = Maintenance.objects.filter(token=request.POST['token'])
    qs.delete()
    qs = Maintenance.objects.all()
    qs = remove_duplicates(qs)
    
  context['services_rendered'] = qs
  
  return render(request, 'vehicle/service_rendered.html', context)

@login_required(login_url='auth/login')
def render_service(request):
  if request.method == 'GET' and request.is_ajax():
    # cust = Customer.objects.get(id =1)
    data_key = [key for key in request.GET.keys()][1]
    data = request.GET.get(data_key).split(' ')
    customer = get_object_or_404(Customer, fullname=request.session['customer'])
    _token = serviceTokenGenerator()
    for dt in data:
      _service = Service.objects.get(id = dt)
      _maintenance = Maintenance.objects.create(owner=customer,service=_service,token=_token)
      _maintenance.save()
    
    print('Its ajax request')
    
    return JsonResponse({'status': 'success', 'status_code': 201, 'data': {'token': _token}})
  return render(request, 'vehicle/maintenance.html')

@login_required(login_url='auth/login')
def search_customers(request):
  qs_services = Service.objects.all()
  queryset = []
  if request.method == 'POST' and not request.is_ajax():
    search_text = request.POST.get('search-text')
    search_type = request.POST.get('search-type')
    
    if search_type == 'name':
      try:
        queryset = Customer.objects.get(fullname = search_text)
      except:
        queryset = None
    
    if search_type == 'phone_number':
      try:

        queryset = Customer.objects.get(phone = search_text)
        
      except:
          queryset = None
    
    if search_type == 'number_plate':
      try:
        queryset = Customer.objects.get(vehicles__vehicle_number_plate = search_text)
      except:
        queryset = None
        
        
    if queryset is None:
      return render(request, 'vehicle/maintenance.html')
  
  print("QUERY: ", queryset)
  
  request.session['customer']  = queryset.fullname if hasattr(queryset, 'fullname') else ''

  context = {
    'data': {
      'customer': queryset,
      'services': qs_services,
    }
  }
  return render(request, 'vehicle/maintenance.html', context)


def render_service_after_registration(request):
  qs_services = Service.objects.all()
  queryset = []
  print('ID', request.session['customerVNumPlate'])

  if request.session['customerVNumPlate'] != '':
    try:
      queryset = Customer.objects.get(vehicles__vehicle_number_plate = request.session['customerVNumPlate'])
    except:
      queryset = None
      
      
  if queryset is None:
    return render(request, 'vehicle/maintenance.html')

  print("QUERY: ", queryset)
  
  request.session['customer']  = queryset.fullname if hasattr(queryset, 'fullname') else ''

  context = {
    'data': {
      'customer': queryset,
      'services': qs_services,
    }
  }
  print(context)
  return render(request, 'vehicle/maintenance.html', context)




#*** Schedule Custom ***#
@login_required(login_url='auth/login')
def maintenance_schedule(request):
  context = {}
  qs = None
  if request.method == 'POST':
    print(request.POST['customer'])
    try:
      customer = Customer.objects.get(id=request.POST['customer'])
      schedule = ScheduleMaintenance.objects.create(customer = customer)
      schedule.save()
    except:
      print('Customer already is in the schedule')
    
  qs = ScheduleMaintenance.objects.all()
  context['customers'] = qs 
  print(context['customers'])
    
  return render(request, 'vehicle/maintenance_schedule.html', context)