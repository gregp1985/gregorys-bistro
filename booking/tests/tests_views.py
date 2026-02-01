from datetime import datetime, time
from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from django.utils import timezone
from booking.models import Booking, Table, OpeningHours
from booking.constants import SLOT_DURATION


class BookingViewTests(TestCase):

    def setUp(self):
        """
        Setup of self function for other tests to use
        """
        self.user = User.objects.create_user(
            username='testuser',
            password='password123'
        )

        self.client.login(
            username='testuser',
            password='password123'
        )

        self.table = Table.objects.create(
            number=1,
            seats=4
        )

        OpeningHours.objects.create(
            weekday=0,
            open_time=time(11, 0),
            close_time=time(23, 0),
        )

        self.monday_date = timezone.localdate().replace(
            year=2026, month=2, day=2
        )

        self.start_time = timezone.make_aware(
            datetime(2026, 2, 2, 13, 0)
        )

    def test_available_slots_returns_slots(self):
        """
        Test that the available slots view returns slots
        """
        url = reverse('booking:available_slots')

        response = self.client.get(url, {
            'date': self.monday_date.isoformat(),
            'party_size':2,
        })

        self.assertEqual(response.status_code, 200)

        data = response.json()
        self.assertIn('slots', data)
        self.assertTrue(len(data['slots']) > 0)
