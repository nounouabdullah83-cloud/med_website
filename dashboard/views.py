from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from services.forms import ServiceForm
from services.models import Service
from booking.models import Booking
from booking.forms import BookingForm

from django.utils import timezone

@login_required
def show_dashboard(request):
    # Get last 6 bookings
    recent_bookings = Booking.objects.all().order_by('-created_at')[:6]
    total_services = Service.objects.count()
    
    # Calculate today's appointments (all bookings scheduled for today)
    today = timezone.localdate()
    today_appointments_count = Booking.objects.all().count()
    
    return render(request, 'dashboard/dashboard.html', {
        'recent_bookings': recent_bookings,
        'total_services': total_services,
        'today_appointments_count': today_appointments_count,
    })

@login_required
def all_bookings(request):
    bookings = Booking.objects.all().order_by('-created_at')
    return render(request, 'dashboard/all_bookings.html', {
        'bookings': bookings
    })

# services dashboard 
@login_required
def add_service(request):
    if request.method == 'POST':
        form = ServiceForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('dashboard:show_all_services')
    else:
        form = ServiceForm()
    return render(request, 'dashboard/add_service.html', {'form': form})

@login_required
def update_service(request, pk):
    service = get_object_or_404(Service, pk=pk)
    if request.method == 'POST':
        form = ServiceForm(request.POST, request.FILES, instance=service)
        if form.is_valid():
            form.save()
            return redirect('dashboard:show_all_services')
    else:
        form = ServiceForm(instance=service)
    return render(request, 'dashboard/update_service.html', {'form': form, 'service': service})

@login_required
def delete_service(request, pk):
    service = get_object_or_404(Service, pk=pk)
    if request.method == 'POST':
        service.delete()
        return redirect('dashboard:show_all_services')
    return render(request, 'dashboard/delete_service.html', {'service': service})

from django.views.decorators.http import require_POST
from django.db import transaction
from statictics.models import BookingStatistic
from decimal import Decimal

@login_required
@require_POST
def booking_done(request, id):
    book = get_object_or_404(Booking, id=id)
    created_date = book.created_at.date()
    service = book.service
    price = Decimal(service.price)

    with transaction.atomic():
        stat, created = BookingStatistic.objects.get_or_create(
            date=created_date,
            service=service,
        )
        stat.completed_count += 1
        stat.total_revenues += price
        stat.save()
        book.delete()
        
    return redirect('dashboard:all_bookings')

@login_required
@require_POST
def booking_cancelled(request, id):
    book = get_object_or_404(Booking, id=id)
    created_date = book.created_at.date()
    service = book.service

    with transaction.atomic():
        stat, created = BookingStatistic.objects.get_or_create(
            date=created_date,
            service=service,
        )
        stat.cancelled_count += 1
        stat.save()
        book.delete()
        
    return redirect('dashboard:all_bookings')

from schedule.models import BusinessDay
from schedule.forms import BusinessDayForm

@login_required
def manage_schedule(request):
    schedule = BusinessDay.objects.all().order_by('day')
    return render(request, 'dashboard/manage_schedule.html', {'schedule': schedule})

@login_required
def update_business_day(request, pk):
    business_day = get_object_or_404(BusinessDay, pk=pk)
    if request.method == 'POST':
        form = BusinessDayForm(request.POST, instance=business_day)
        if form.is_valid():
            form.save()
            return redirect('dashboard:manage_schedule')
    else:
        form = BusinessDayForm(instance=business_day)
    return render(request, 'dashboard/update_business_day.html', {
        'form': form, 
        'business_day': business_day
    })

@login_required
def show_all_services(request):
    services = Service.objects.all()
    return render(request, 'dashboard/show_all_services.html', {'services':services})

@login_required
def add_booking_manual(request):
    if request.method == 'POST':
        form = BookingForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('/dashboard/')
        
    else:
        form = BookingForm()
    
    return render(request, 'dashboard/add_booking_manual.html', {'form':form})

