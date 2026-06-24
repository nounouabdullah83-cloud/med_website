from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from django.utils import timezone
from booking.models import Booking
from services.models import Service
from statictics.models import BookingStatistic
import datetime

class BookingStatisticsTests(TestCase):
    def setUp(self):
        # Create user
        self.user = User.objects.create_user(username='admin', password='password')
        self.client = Client()
        # Create service
        self.service = Service.objects.create(
            name="Consultation",
            description="General consult",
            price=150.00
        )
        # Log user in
        self.client.login(username='admin', password='password')

    def test_booking_completion_creates_statistics_and_deletes_booking(self):
        # Create booking
        booking = Booking.objects.create(
            service=self.service,
            full_name="John Doe",
            age=30,
            email="john@example.com",
            phone_number="12345678",
            appointment_date=datetime.date.today(),
            appointment_time=datetime.time(10, 0),
            status='pending'
        )
        
        # Call booking_done view
        response = self.client.post(reverse('dashboard:booking_done', args=[booking.id]))
        self.assertEqual(response.status_code, 302) # Redirect to all_bookings

        # Assert booking is deleted from Booking table
        self.assertFalse(Booking.objects.filter(id=booking.id).exists())

        # Assert BookingStatistic is created
        self.assertTrue(BookingStatistic.objects.filter(service=self.service, date=booking.created_at.date()).exists())
        stat = BookingStatistic.objects.get(service=self.service, date=booking.created_at.date())
        self.assertEqual(stat.completed_count, 1)
        self.assertEqual(stat.cancelled_count, 0)
        self.assertEqual(stat.total_revenues, 150.00)

    def test_booking_cancellation_creates_statistics_and_deletes_booking(self):
        # Create booking
        booking = Booking.objects.create(
            service=self.service,
            full_name="Jane Doe",
            age=25,
            email="jane@example.com",
            phone_number="87654321",
            appointment_date=datetime.date.today(),
            appointment_time=datetime.time(11, 0),
            status='pending'
        )
        
        # Call booking_cancelled view
        response = self.client.post(reverse('dashboard:booking_cancelled', args=[booking.id]))
        self.assertEqual(response.status_code, 302)

        # Assert booking is deleted
        self.assertFalse(Booking.objects.filter(id=booking.id).exists())

        # Assert BookingStatistic is created
        stat = BookingStatistic.objects.get(service=self.service, date=booking.created_at.date())
        self.assertEqual(stat.completed_count, 0)
        self.assertEqual(stat.cancelled_count, 1)
        self.assertEqual(stat.total_revenues, 0.00)

    def test_business_info_aggregates_correctly(self):
        # Create manual/legacy/accumulated statistic records
        today = datetime.date.today()
        BookingStatistic.objects.create(
            date=today,
            service=self.service,
            completed_count=3,
            cancelled_count=1,
            total_revenues=450.00
        )

        # Create one pending booking (should be counted in stats too)
        Booking.objects.create(
            service=self.service,
            full_name="Bob",
            age=40,
            appointment_date=today,
            appointment_time=datetime.time(14, 0),
            status='pending'
        )

        # Fetch stats page
        response = self.client.get(reverse('statictics:business_info'))
        self.assertEqual(response.status_code, 200)

        # Check total calculations in context
        self.assertEqual(response.context['total_bookings'], 5) # 3 completed + 1 cancelled + 1 pending
        self.assertEqual(response.context['total_revenues'], 450.00)
        self.assertEqual(response.context['completed_count'], 3)
        
        # Check service stats
        service_stats = response.context['service_stats']
        self.assertEqual(len(service_stats), 1)
        self.assertEqual(service_stats[0]['name'], "Consultation")
        self.assertEqual(service_stats[0]['revenues'], 450.00)
        self.assertEqual(service_stats[0]['bookings'], 5)
        self.assertEqual(service_stats[0]['completed'], 3)

        # Check status breakdown
        status_stats = response.context['status_stats']
        self.assertEqual(status_stats['completed'], 3)
        self.assertEqual(status_stats['cancelled'], 1)
        self.assertEqual(status_stats['pending'], 1)
