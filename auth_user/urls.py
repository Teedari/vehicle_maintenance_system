from django.urls import path
from .views import signIn, signOut

app_name = 'auth_user'

urlpatterns = [
 path( 'login', signIn,  name='signIn'),
 path('logout', signOut, name='signOut')
]