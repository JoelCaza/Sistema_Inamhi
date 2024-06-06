from django.urls import path
from . import views

urlpatterns = [
    path('', views.ticket_list, name='ticket_list'),
    # Otros patrones de URL para las vistas de tickets
]
