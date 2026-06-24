from django.db import migrations
import datetime

def populate_days(apps, schema_editor):
    BusinessDay = apps.get_model('schedule', 'BusinessDay')
    
    # Check if they are already populated
    if BusinessDay.objects.exists():
        return
        
    days = [
        (0, datetime.time(9, 0), datetime.time(17, 0), False),  # Monday
        (1, datetime.time(9, 0), datetime.time(17, 0), False),  # Tuesday
        (2, datetime.time(9, 0), datetime.time(17, 0), False),  # Wednesday
        (3, datetime.time(9, 0), datetime.time(17, 0), False),  # Thursday
        (4, datetime.time(9, 0), datetime.time(17, 0), False),  # Friday
        (5, None, None, True),                                  # Saturday
        (6, None, None, True),                                  # Sunday
    ]
    
    for day_num, open_time, close_time, closed in days:
        BusinessDay.objects.get_or_create(
            day=day_num,
            defaults={
                'opening_time': open_time,
                'closing_time': close_time,
                'is_closed': closed
            }
        )

def remove_days(apps, schema_editor):
    BusinessDay = apps.get_model('schedule', 'BusinessDay')
    BusinessDay.objects.all().delete()

class Migration(migrations.Migration):

    dependencies = [
        ('schedule', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(populate_days, reverse_code=remove_days),
    ]
