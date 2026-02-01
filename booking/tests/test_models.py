from datetime import datetime, time
from django.test import TestCase
from django.contrib.auth.models import User
from django.utils import timezone
from booking.models import Booking, Table, OpeningHours
from booking.constants import SLOT_DURATION


class BookingModelTests(TestCase):

    def setUp(self):
        """
        Setup of User, Table, Opening Hours and date for tests to use
        """
        self.user = User.objects.create_user(
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
            close_time=time(23, 0)
        )

        self.date = timezone.make_aware(
            datetime(2026, 2, 2, 13, 0)
        )

    def test_booking_saves_time_range_and_reference(self):
        """
        Test to check time range and booking reference are asaved on booking
        """
        booking = Booking.objects.create(
            table=self.table,
            name=self.user,
            party_size=2,
            start_time=self.date,
        )

        self.assertIsNotNone(booking.reference)
        self.assertEqual(
            booking.time_range[0],
            booking.start_time
        )
        self.assertEqual(
            booking.time_range[1],
            booking.start_time + SLOT_DURATION
        )
