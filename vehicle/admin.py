from django.contrib import admin

from .models import Customer, Vehicle, Service, Maintenance

# Register your models here.

admin.site.register(Vehicle)
admin.site.register(Customer)
admin.site.register(Service)
admin.site.register(Maintenance)
