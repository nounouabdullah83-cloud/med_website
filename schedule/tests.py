from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from schedule.models import BusinessDay
import datetime

class ScheduleTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_superuser(username='admin', password='password')
        self.client = Client()
        self.client.login(username='admin', password='password')
        # Create a business day
        self.business_day = BusinessDay.objects.get_or_create(
            day=0,
            defaults={
                'opening_time': datetime.time(9, 0),
                'closing_time': datetime.time(17, 0),
                'is_closed': False
            }
        )[0]

    def test_update_hours(self):
        response = self.client.post(
            reverse('dashboard:update_business_day', args=[self.business_day.pk]),
            data={
                'day': 0,
                'opening_time': '08:00',
                'closing_time': '16:00',
                'is_closed': ''
            }
        )
        self.assertEqual(response.status_code, 302)
        self.business_day.refresh_from_db()
        self.assertEqual(self.business_day.opening_time, datetime.time(8, 0))
        self.assertEqual(self.business_day.closing_time, datetime.time(16, 0))
        self.assertFalse(self.business_day.is_closed)

    def test_update_to_closed(self):
        response = self.client.post(
            reverse('dashboard:update_business_day', args=[self.business_day.pk]),
            data={
                'day': 0,
                'opening_time': '09:00',
                'closing_time': '17:00',
                'is_closed': 'on'
            }
        )
        self.assertEqual(response.status_code, 302)
        self.business_day.refresh_from_db()
        self.assertTrue(self.business_day.is_closed)
        self.assertIsNone(self.business_day.opening_time)
        self.assertIsNone(self.business_day.closing_time)

    def test_invalid_open_with_empty_times(self):
        response = self.client.post(
            reverse('dashboard:update_business_day', args=[self.business_day.pk]),
            data={
                'day': 0,
                'opening_time': '',
                'closing_time': '',
                'is_closed': ''
            }
        )
        self.assertEqual(response.status_code, 200) # Re-renders form due to errors
        form = response.context['form']
        self.assertIn('opening_time', form.errors)
        self.assertIn('closing_time', form.errors)

    def test_invalid_closing_before_opening(self):
        response = self.client.post(
            reverse('dashboard:update_business_day', args=[self.business_day.pk]),
            data={
                'day': 0,
                'opening_time': '12:00',
                'closing_time': '10:00',
                'is_closed': ''
            }
        )
        self.assertEqual(response.status_code, 200)
        form = response.context['form']
        self.assertIn('closing_time', form.errors)
        self.assertEqual(form.errors['closing_time'][0], 'Closing time must be after opening time.')
