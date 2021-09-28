from django.urls import path
from .views import index, view_pdf

app_name = 'pdf_writer'


urlpatterns = [
  path('', index, name='home'),
  path('<str:token>/', view_pdf, name='preview')
]
