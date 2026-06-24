from django.urls import path
from . import views

app_name = 'statictics'

urlpatterns = [
    path('', views.business_info, name='business_info'),
]
