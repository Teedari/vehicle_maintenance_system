from django.http.response import HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404, render, reverse

from payment.models import Payment
from .forms import PaymentForm
from django.conf import settings
# Create your views here.

def initiatePayment(request):
  form = PaymentForm()
  context = {}
  if request.method == 'POST':
    form = PaymentForm(request.POST)
    if form.is_valid():
      payment = form.save()
      context['paystack_public_key'] = settings.PAYSTACK_PUBLIC_KEY
      context['payment'] = payment
      return render(request, 'payment/make_payment.html', context)
    
  context['form'] = form
  return render(request, 'payment/index.html', context)


def makePayment(request):
  return render(request, 'payment/make_payment.html')


def verifyPayment(request, ref:str):
   payment = get_object_or_404(Payment, ref=ref)
   verified = payment.verify_payment()
   return HttpResponseRedirect(reverse())