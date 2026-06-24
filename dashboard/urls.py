from django.urls import path
from . import views

app_name = 'dashboard'

urlpatterns = [
    path('', views.show_dashboard, name='show_dashboard'),
    path('all_services/', views.show_all_services, name='show_all_services'),
    path('bookings/', views.all_bookings, name='all_bookings'),
    path('add_booking_manual/', views.add_booking_manual, name='add_booking_manual'),
    # services section
    path('add/', views.add_service, name='add_service'),
    path('update/<int:pk>/', views.update_service, name='update_service'),
    path('delete/<int:pk>/', views.delete_service, name='delete_service'),
    path('booking_done/<int:id>/', views.booking_done, name='booking_done'),
    path('booking_cancelled/<int:id>/', views.booking_cancelled, name='booking_cancelled'),
    # schedule section
    path('schedule/', views.manage_schedule, name='manage_schedule'),
    path('schedule/update/<int:pk>/', views.update_business_day, name='update_business_day'),
]
