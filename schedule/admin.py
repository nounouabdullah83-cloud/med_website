from django.contrib import admin
from .models import BusinessDay

@admin.register(BusinessDay)
class BusinessDayAdmin(admin.ModelAdmin):
    list_display = ('day', 'opening_time', 'closing_time', 'is_closed')
    list_editable = ('opening_time', 'closing_time', 'is_closed')
