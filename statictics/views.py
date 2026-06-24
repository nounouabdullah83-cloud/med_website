from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.db.models import Sum, Count
from django.utils import timezone
from datetime import timedelta
from booking.models import Booking
from services.models import Service
from statictics.models import BookingStatistic

@login_required
def business_info(request):
    period = request.GET.get('period', 'year')
    now = timezone.now()
    
    # The statistics reset every year: show only current year data
    start_of_year = now.replace(month=1, day=1, hour=0, minute=0, second=0, microsecond=0)
    
    if period == 'week':
        start_date = now - timedelta(days=7)
    elif period == 'month':
        start_date = now - timedelta(days=30)
    else: # year
        start_date = start_of_year
        
    start_date_only = start_date.date()
    
    # Filtered BookingStatistic (completed, cancelled, revenues)
    filtered_stats = BookingStatistic.objects.filter(date__gte=start_date_only)
    
    # Filtered active bookings (pending)
    pending_bookings = Booking.objects.filter(created_at__gte=start_date, status='pending')
    
    # Total cards
    completed_count = filtered_stats.aggregate(total=Sum('completed_count'))['total'] or 0
    cancelled_count = filtered_stats.aggregate(total=Sum('cancelled_count'))['total'] or 0
    pending_count = pending_bookings.count()
    
    total_revenues = filtered_stats.aggregate(total=Sum('total_revenues'))['total'] or 0
    total_bookings = completed_count + cancelled_count + pending_count
    
    # Service performance
    services = Service.objects.all()
    service_stats = []
    for service in services:
        s_stats = filtered_stats.filter(service=service)
        s_completed = s_stats.aggregate(total=Sum('completed_count'))['total'] or 0
        s_cancelled = s_stats.aggregate(total=Sum('cancelled_count'))['total'] or 0
        s_revenues = s_stats.aggregate(total=Sum('total_revenues'))['total'] or 0
        s_pending = pending_bookings.filter(service=service).count()
        
        service_stats.append({
            'name': service.name,
            'revenues': s_revenues,
            'bookings': s_completed + s_cancelled + s_pending,
            'completed': s_completed
        })
        
    # Appointment statuses
    status_stats = {
        'completed': completed_count,
        'pending': pending_count,
        'cancelled': cancelled_count,
    }
    
    context = {
        'total_revenues': total_revenues,
        'total_bookings': total_bookings,
        'completed_count': completed_count,
        'service_stats': service_stats,
        'status_stats': status_stats,
        'period': period,
    }
    return render(request, 'statictics/business_info.html', context)
