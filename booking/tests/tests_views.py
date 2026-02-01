from datetime import datetime, time
from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from django.utils import timezone
from booking.models import Booking, Table, OpeningHours


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
        self.table2 = Table.objects.create(
            number=2,
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

    # Available Slots
    def test_available_slots_returns_slots(self):
        """
        Test that the available slots view returns slots
        """
        url = reverse('booking:available_slots')

        response = self.client.get(url, {
            'date': self.monday_date.isoformat(),
            'party_size': 2,
        })

        self.assertEqual(response.status_code, 200)

        data = response.json()
        self.assertIn('slots', data)
        self.assertTrue(len(data['slots']) > 0)

    def test_available_slots_returns_empty_for_invalid_date(self):
        """
        Test to make sure no slots returned for invalid date
        """
        url = reverse('booking:available_slots')

        response = self.client.get(url, {
            'date': 'invalid-date',
            'party_size': 2,
        })

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['slots'], [])

    def test_available_slots_excludes_existing_booking(self):
        """
        Test to ensure available slots exclude existing bookings
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

        url = reverse('booking:available_slots')

        response = self.client.get(url, {
            'date': self.monday_date.isoformat(),
            'party_size': 2,
        })

        slots = [
            slot['value']
            for slot in response.json()['slots']
        ]

        self.assertNotIn(self.start_time.isoformat(), slots)

    # Make Booking
    def test_make_booking_page_loads(self):
        """
        Test to ensure the make booking poage loads correctly
        """
        url = reverse('booking:booking')

        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Make a Booking')

    def test_make_a_booking_creates_booking(self):
        """
        Test to check a booking is actually created on valid submission
        """
        url = reverse('booking:booking')

        response = self.client.post(url, {
            'date': self.monday_date.isoformat(),
            'party_size': 2,
            'slot': self.start_time.isoformat(),
            'allergies': 'Peanuts',
        })

        self.assertEqual(response.status_code, 302)
        self.assertEqual(Booking.objects.count(), 1)

        booking = Booking.objects.first()
        self.assertEqual(booking.name, self.user)
        self.assertEqual(booking.party_size, 2)
        self.assertEqual(booking.start_time, self.start_time)

    # Cancel Booking
    def test_cancel_booking_sets_status(self):
        """
        Test to check that when a user cancels a booking the status is changed
        """
        booking = Booking.objects.create(
            table=self.table,
            name=self.user,
            party_size=2,
            start_time=self.start_time,
        )

        url = reverse(
            'booking:cancel_booking',
            args=[booking.id]
        )

        response = self.client.post(url)

        booking.refresh_from_db()

        self.assertEqual(response.status_code, 302)
        self.assertEqual(booking.status, 'CANCELLED')

    # Edit Booking
    """
    Test to check the edit booking page loads correctly
    """
    def test_edit_booking_page_loads(self):
        booking = Booking.objects.create(
            table=self.table,
            name=self.user,
            party_size=2,
            start_time=self.start_time,
        )

        url = reverse(
            'booking:edit_booking',
            args=[booking.id]
        )

        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Editing Booking')

    def test_edit_booking_updates_time(self):
        """
        Test to check that if the edit booking time is updated and saved,
        it updates the booking
        """
        booking = Booking.objects.create(
            table=self.table,
            name=self.user,
            party_size=2,
            start_time=self.start_time,
        )

        new_time = timezone.make_aware(
            datetime(2026, 2, 2, 14, 0)
        )

        url = reverse(
            'booking:edit_booking',
            args=[booking.id]
        )

        response = self.client.post(url, {
            'date': self.monday_date.isoformat(),
            'party_size': 2,
            'slot': new_time.isoformat(),
            'allergies': '',
        })

        self.assertEqual(response.status_code, 302)

        booking.refresh_from_db()

        self.assertEqual(booking.start_time, new_time)
