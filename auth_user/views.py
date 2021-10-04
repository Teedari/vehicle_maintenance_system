from django.http.response import HttpResponseRedirect
from auth_user.forms import UserLoginForms
from django.shortcuts import render, reverse
from django.contrib.auth import login, authenticate, logout
# Create your views here.


def signIn(request):
  form = None
  if request.method == "POST":
    form = UserLoginForms(request.POST)
    
    if form.is_valid():
      # print(form.cleaned_data)
      auth = authenticate(**form.cleaned_data)
      if auth is not None:
        login(request, user = auth)
        print(auth)
        return HttpResponseRedirect(reverse('vehicle:dashboard'))
      
  return render(request, 'auth_user/login.html')





def signOut(request):
  try:
      logout(request)
      del request.session['customer']
      del request.session['count']
  except:
    return
  finally:
    return HttpResponseRedirect(reverse('auth_user:signIn'))
    
  # logout(request)