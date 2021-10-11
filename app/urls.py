from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('', include('vehicle.urls', namespace='vehicle')),
    path('auth/', include('auth_user.urls', namespace='authentication')),
    path('payment/', include('payment.urls', namespace='payment')),
    path('pdf/', include('pdf_writer.urls', namespace='pdf')),
    path('admin/', admin.site.urls),
]


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)