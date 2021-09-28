from vehicle.models import Service
from django.http.response import JsonResponse

## Signals 


def get_request_vehicle(func):
  def wrapper(request, *args, **kwargs):
    
    if request.method == 'GET' and request.is_ajax():
      if request.GET.get('type') == 'delete':
        del_service = Service.objects.get(id = request.GET.get('ID'))
        del_service.delete()
        _services = Service.objects.all()
        return JsonResponse({"status": 'success deletion', 'data': list(_services.values())})
      
    return func(request, *args, **kwargs)
  return wrapper