from django.urls import path
from . import views

app_name = 'booking'

urlpatterns = [
    path('submit/', views.submit_booking, name='submit_booking'),
]
