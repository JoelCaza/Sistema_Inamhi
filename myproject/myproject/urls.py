from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('myapp.app_url')),  # Se incluye el archivo de URLs de myapp
    path('ticket/', include('tickets.urls')),  # Se incluye el archivo de URLs de tickets
    path('accounts/', include('django.contrib.auth.urls'))
]
