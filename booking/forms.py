from django import forms
from .models import Booking

from datetime import date
from schedule.models import BusinessDay

class BookingForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            if isinstance(field.widget, forms.CheckboxInput):
                field.widget.attrs.update({'class': 'form-check-input'})
            else:
                field.widget.attrs.update({'class': 'form-control'})

    class Meta:
        model = Booking
        fields = ['service', 'full_name', 'age', 'email', 'phone_number', 'appointment_date', 'appointment_time', 'note']
        widgets = {
            'note': forms.Textarea(attrs={'rows': 3, 'placeholder': 'Simple note...'}),
            'appointment_date': forms.DateInput(attrs={'type': 'date', 'min': date.today().isoformat()}),
            'appointment_time': forms.TimeInput(attrs={'type': 'time'}),
        }

    def clean(self):
        cleaned_data = super().clean()
        appointment_date = cleaned_data.get('appointment_date')
        appointment_time = cleaned_data.get('appointment_time')

        if appointment_date and appointment_time:
            # Check if date is in the past
            if appointment_date < date.today():
                raise forms.ValidationError("You cannot book an appointment in the past.")

            # Get business day for the selected date
            weekday = appointment_date.weekday()
            try:
                business_day = BusinessDay.objects.get(day=weekday)
                if business_day.is_closed:
                    raise forms.ValidationError(f"We are closed on {business_day.get_day_display()}.")
                
                if business_day.opening_time and business_day.closing_time:
                    if not (business_day.opening_time <= appointment_time <= business_day.closing_time):
                        raise forms.ValidationError(
                            f"Appointment must be between {business_day.opening_time.strftime('%H:%M')} "
                            f"and {business_day.closing_time.strftime('%H:%M')} on this day."
                        )
            except BusinessDay.DoesNotExist:
                # If day is not defined, assume closed or handled as error
                raise forms.ValidationError("Business hours for this day are not configured yet.")

            # Check if slot is already booked
            if Booking.objects.filter(
                appointment_date=appointment_date,
                appointment_time=appointment_time
            ).exclude(status='cancelled').exists():
                raise forms.ValidationError("This appointment slot is already taken. Please choose another time.")

        return cleaned_data
