from django.urls import path
from . import views

app_name = 'services'

urlpatterns = [
    path('', views.show_all_services, name='show_all_services'),
    path('service/<int:id>/', views.service_detials, name='service_detials'),
]
