from django.shortcuts import render, redirect, get_object_or_404
from .models import Service
from .forms import ServiceForm

def show_all_services(request):
    services = Service.objects.all()
    return render(request, 'services/show_all_services.html', {'services': services})

def service_detials(request, id):
    service = get_object_or_404(Service, id=id)
    return render(request, 'services/service_detials.html', {'service':service})