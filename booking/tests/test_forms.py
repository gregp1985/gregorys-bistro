from datetime import datetime, time
from django.test import TestCase
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.utils import timezone
from booking.forms import BookingForm
from booking.models import Booking, Table, OpeningHours


class BookingFormTests(TestCase):

    def setUp(self):
        """
        Setup of User, Tables, Opening Hours and dates and
        times for the rest of the tests
        """
        self.user = User.objects.create_user(
            username='testuser',
            password='password123'
        )

        self.table = Table.objects.create(number=1, seats=4)
        self.table2 = Table.objects.create(number=2, seats=4)

        OpeningHours.objects.create(
            weekday=0,
            open_time=time(11, 0),
            close_time=time(23, 0),
        )

        self.date = timezone.localdate().replace(
            year=2026, month=2, day=2
        )

        self.start_time = timezone.make_aware(
            datetime(2026, 2, 2, 13, 0)
        )

    def test_form_valid_data_creates_booking(self):
        """
        Test to confirm the form is valid when valid
        data is entered in it and submitted
        """
        form = BookingForm(
            data={
                'date': self.date,
                'party_size': 2,
                'slot': self.start_time.isoformat(),
                'allergies': '',
            },
            user=self.user
        )

        form.fields['slot'].choices = [
            (self.start_time.isoformat(), self.start_time.isoformat())
        ]

        self.assertTrue(form.is_valid(), form.errors)

        booking = form.save()

        self.assertEqual(booking.name, self.user)
        self.assertEqual(booking.party_size, 2)
        self.assertEqual(booking.start_time, self.start_time)
        self.assertIsNotNone(booking.table)

    def test_form_invalid_without_slot(self):
        """
        Test to confirm the form is not valid if a slot is not selected
        """
        form = BookingForm(
            data={
                'date': self.date,
                'party_size': 2,
                'allergies': '',
            },
            user=self.user
        )

        self.assertFalse(form.is_valid())
        self.assertIn('slot', form.errors)

    def test_form_raises_error_when_no_tables_available(self):
        """
        Test that an error is raised if no tables are available on a set day
        """
        Booking.objects.create(
            table=self.table,
            name=self.user,
            party_size=2,
            start_time=self.start_time,
        )
        Booking.objects.create(
            table=self.table2,
            name=self.user,
            party_size=2,
            start_time=self.start_time,
        )

        form = BookingForm(
            data={
                'date': self.date,
                'party_size': 2,
                'slot': self.start_time.isoformat(),
                'allergies': '',
            },
            user=self.user
        )

        form.fields['slot'].choices = [
            (self.start_time.isoformat(), self.start_time.isoformat())
        ]

        self.assertTrue(form.is_valid())

        with self.assertRaisesMessage(
            ValidationError,
            'That time is no longer available'
        ):
            form.save()

    def test_edit_booking_excludes_self_from_overlap_check(self):
        """
        Test to check that when editing a booking the original booking is
        excluded from the overlap check
        """
        booking = Booking.objects.create(
            table=self.table,
            name=self.user,
            party_size=2,
            start_time=self.start_time,
        )

        form = BookingForm(
            data={
                'date': self.date.isoformat(),
                'party_size': 2,
                'slot': self.start_time.isoformat(),
                'allergies': '',
            },
            instance=booking,
            user=self.user
        )

        self.assertTrue(form.is_valid())

        updated_booking = form.save()

        self.assertEqual(updated_booking.start_time, self.start_time)
        self.assertEqual(updated_booking.table, self.table)
