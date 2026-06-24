from django.shortcuts import render, redirect
from django.contrib import messages
from django.db import transaction
from .forms import BookingForm
from services.models import Service
from schedule.models import BusinessDay

def submit_booking(request):
    if request.method == 'POST':
        form = BookingForm(request.POST)
        if form.is_valid():
            try:
                with transaction.atomic():
                    form.save()
                messages.success(request, "Your booking has been submitted successfully!")
                return redirect('core:landing_page')
            except Exception as e:
                messages.error(request, "An unexpected error occurred. Please try again.")
        else:
            messages.error(request, "There was an error with your booking. Please check the form and try again.")
            # Re-render landing page with form errors
            few_services = Service.objects.all().order_by('?')[:3]
            schedule = BusinessDay.objects.all().order_by('day')
            return render(request, 'landing_page/landing_page.html', {
                'booking_form': form,
                'few_services': few_services,
                'schedule': schedule
            })
    return redirect('core:landing_page')
