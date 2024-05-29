# app_url.py
from django.urls import path
from . import views

urlpatterns = [

    path('', views.model_list, name='model_list'),
    path('admin', views.login_required, name='login'),
    path('create/', views.model_create, name='model_create'),
    path('<int:pk>/', views.model_detail, name='model_detail'),
    path('<int:pk>/update/', views.model_update, name='model_update'),
    path('<int:pk>/delete/', views.model_delete, name='model_delete'),
    path('<int:pk>/delete/confirm/', views.model_confirm_delete, name='model_confirm_delete'),
    path('salir/', views.salir, name="salir")

]


