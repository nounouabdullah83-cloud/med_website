from django.shortcuts import render
from booking.forms import BookingForm
from services.models import Service
import random

from schedule.models import BusinessDay

def landing_page(request):
    form = BookingForm()
    few_services = Service.objects.all().order_by('?')[:3]
    schedule = BusinessDay.objects.all().order_by('day')

    data = {
        'booking_form': form,
        'few_services': few_services,
        'schedule': schedule
    }
    return render(request, 'landing_page/landing_page.html', data)
