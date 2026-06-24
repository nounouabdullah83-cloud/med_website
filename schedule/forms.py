from django import forms
from schedule.models import BusinessDay

class BusinessDayForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            if isinstance(field.widget, forms.CheckboxInput):
                field.widget.attrs.update({'class': 'form-check-input'})
            else:
                field.widget.attrs.update({'class': 'form-control'})

    def clean(self):
        cleaned_data = super().clean()
        is_closed = cleaned_data.get('is_closed')
        opening_time = cleaned_data.get('opening_time')
        closing_time = cleaned_data.get('closing_time')

        if not is_closed:
            if not opening_time:
                self.add_error('opening_time', 'Opening time is required when the business day is open.')
            if not closing_time:
                self.add_error('closing_time', 'Closing time is required when the business day is open.')
            if opening_time and closing_time and opening_time >= closing_time:
                self.add_error('closing_time', 'Closing time must be after opening time.')
        else:
            cleaned_data['opening_time'] = None
            cleaned_data['closing_time'] = None

        return cleaned_data

    class Meta:
        model = BusinessDay
        fields = ['day', 'opening_time', 'closing_time', 'is_closed']
        widgets = {
            'opening_time': forms.TimeInput(attrs={'type': 'time'}),
            'closing_time': forms.TimeInput(attrs={'type': 'time'}),
        }
