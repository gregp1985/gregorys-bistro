from datetime import datetime, time
from django.test import TestCase
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.db.utils import IntegrityError
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

        self.start_time = timezone.make_aware(
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
            start_time=self.start_time,
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

    def test_booking_outside_opening_hours_raises_validation_error(self):
        """
        Test that booking outside of Opening Hours fails
        with a Validation Error
        """
        early_time = timezone.make_aware(
            datetime(2026, 2, 2, 9, 0)
        )

        booking = Booking(
            table=self.table,
            name=self.user,
            party_size=2,
            start_time=early_time,
        )

        with self.assertRaises(ValidationError):
            booking.clean()

    def test_booking_on_closed_day_raises_validation_error(self):
        """
        Test to check that a validation error is returned if booking
        on a closed day
        """
        closed_day = timezone.make_aware(
            datetime(2026, 2, 3, 13, 0)
        )

        booking = Booking(
            table=self.table,
            name=self.user,
            party_size=2,
            start_time=closed_day
        )

        with self.assertRaises(ValidationError):
            booking.clean()

    def test_double_booking_same_table_is_blocked(self):
        """
        Test to check tables cannot be double booked
        """
        Booking.objects.create(
            table=self.table,
            name=self.user,
            party_size=2,
            start_time=self.start_time,
        )

        with self.assertRaises(IntegrityError):
            Booking.objects.create(
                table=self.table,
                name=self.user,
                party_size=2,
                start_time=self.start_time,
            )

    def test_overlapping_booking_different_table_is_allowed(self):
        """
        Test to confirm overlapping booking on different tables are allowed
        """
        other_table = Table.objects.create(
            number=2,
            seats=4
        )

        Booking.objects.create(
            table=self.table,
            name=self.user,
            party_size=2,
            start_time=self.start_time,
        )

        booking = Booking.objects.create(
            table=other_table,
            name=self.user,
            party_size=2,
            start_time=self.start_time,
        )

        self.assertIsNotNone(booking.pk)

    def test_naive_datetime_is_made_aware_on_save(self):
        """
        Test to confirm naive times are made aware on save
        """
        naive_time = datetime(2026, 2, 2, 14, 0)

        booking = Booking.objects.create(
            table=self.table,
            name=self.user,
            party_size=2,
            start_time=naive_time,
        )

        self.assertTrue(timezone.is_aware(booking.start_time))
