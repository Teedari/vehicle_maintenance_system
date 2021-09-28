from django.http.response import HttpResponse
from django.shortcuts import render
from django.template.loader import get_template
from xhtml2pdf import pisa
from io import BytesIO
from django.views import View
from vehicle.models import Maintenance
# Create your views here.


def render_to_pdf(_template, _context={}):
  template = get_template(_template)
  html = template.render(_context)
  result  = BytesIO()
  bytes_io = BytesIO(html.encode("ISO-8859-1"))
  pdf = pisa.pisaDocument(bytes_io, result)
  
  if not pdf.err:
    return HttpResponse(result.getvalue(), content_type='application/pdf')
  
  return None



def index(request):
  
  return render(request, 'pdf_writer/index.html')


def view_pdf(request, token:str):
  print(token)
  _maintenance = Maintenance.objects.filter(token=token)
  _total = 0
  for i in range(len(_maintenance)):
    _total += _maintenance[i].amount
    
  print(_maintenance)
  print('Total: ', _total)
  
  if request.method == 'GET':
    pdf = render_to_pdf('pdf_writer/pdf_template.html', {'data': _maintenance, 'singleton': _maintenance[0], 'total': _total})
  
  return HttpResponse(pdf, content_type='application/pdf')
  
  # return render(request, 'pdf_writer/pdf_template.html')
