from datetime import datetime, time
from django.test import TestCase
from django.contrib.auth.models import User
from django.utils import timezone
from booking.forms import BookingForm
from booking.models import Table, OpeningHours


class BookingFormTests(TestCase):

    def setUp(self):
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
