from django.urls import path
from .views import home, list_all_services_rendered, vehicle_register, service, list_all_customers, render_service, search_customers, list_all_services_rendered, maintenance_schedule, render_service_after_registration, create_new_user


app_name='vehicle'

urlpatterns = [
  path('', home, name='dashboard'),
  path('vehicle/user/create', create_new_user, name='create_new_user'),
  path('vehicle/register', vehicle_register, name='vehicle_register'),
  path('vehicle/customers', list_all_customers, name='list_of_customers'),
  path('vehicle/customers/register/render/serivce', render_service_after_registration, name='register_render_service'),
  path('vehicle/customers/query', search_customers, name='search_customer'),
  path('vehicle/customers/render/service', render_service, name='render_service'),
  path('vehicle/customers/services/rendered', list_all_services_rendered, name='list_of_services_rendered'),
  path('vehicle/service', service, name='service'),
  path('vehicle/maintenance/shedule', maintenance_schedule, name='maintenance_schedule'),
]