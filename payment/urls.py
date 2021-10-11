from django.urls import path
from .views import initiatePayment, makePayment, verifyPayment

app_name = 'payment'

urlpatterns = [
  path('', initiatePayment, name='home'),
  path('create', makePayment, name='make_payment'),
  path('<str:ref>/verify', verifyPayment, name='verify_payment')
  # path('payment/')
]