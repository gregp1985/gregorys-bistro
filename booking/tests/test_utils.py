from datetime import datetime, time, timedelta
from django.test import TestCase
from django.utils import timezone
from django.contrib.auth.models import User
from booking.models import Table, OpeningHours, Booking
from booking.utils import get_available_slots


class GetAvailableSlotsTests(TestCase):

    def setUp(self):
        """
        Set up of User and weekday so tests can use these torun
        """
        self.user = User.objects.create_user(
            username='tester',
            password='pass'
        )

        # Tomorrow (safe from "past time" logic)
        self.date = timezone.localdate() + timedelta(days=1)
        self.weekday = self.date.weekday()

        # Opening hours for that weekday
        OpeningHours.objects.create(
            weekday=self.weekday,
            open_time=time(11, 0),
            close_time=time(23, 0),
        )

        # Tables
        self.table_2 = Table.objects.create(number=1, seats=2)
        self.table_4 = Table.objects.create(number=2, seats=4)

    def test_returns_slots_when_tables_available(self):
        """
        Test to confirm slots are returned when tables are available
        """
        slots = get_available_slots(
            date=self.date,
            party_size=2
        )

        self.assertTrue(slots)
        self.assertIsInstance(slots[0], datetime)

    def test_no_slots_when_no_tables_big_enough(self):
        """
        Tests that if no tables are big enough for
        the party size no slots are returned
        """
        slots = get_available_slots(
            date=self.date,
            party_size=10
        )

        self.assertEqual(slots, [])

    def test_excludes_slot_when_table_is_booked(self):
        """
        Tests that slots are not provided if no tables available
        """
        start = timezone.make_aware(
            datetime.combine(self.date, time(13, 0))
        )

        Booking.objects.create(
            table=self.table_4,
            name=self.user,
            party_size=4,
            start_time=start,
        )

        slots = get_available_slots(
            date=self.date,
            party_size=4
        )

        self.assertNotIn(start, slots)

    def test_exclude_booking_when_editing(self):
        """
        Test that when editing an existing booking, its own slot
        should still appear as available.
        """
        start = timezone.make_aware(
            datetime.combine(self.date, time(13, 0))
        )

        booking = Booking.objects.create(
            table=self.table_4,
            name=self.user,
            party_size=4,
            start_time=start,
        )

        slots = get_available_slots(
            date=self.date,
            party_size=4,
            exclude_bookings=Booking.objects.filter(pk=booking.pk),
        )

        self.assertIn(start, slots)

    def test_slot_duration_respected_near_closing(self):
        """
        Test that slots that would overflow past closing time
        must not be returned.
        """
        late_start = timezone.make_aware(
            datetime.combine(self.date, time(22, 0))
        )

        slots = get_available_slots(
            date=self.date,
            party_size=2
        )

        self.assertNotIn(late_start, slots)

    def test_returns_empty_list_when_closed(self):
        """
        Tests that times outside of opening hours are not returned
        """
        OpeningHours.objects.filter(weekday=self.weekday).delete()

        slots = get_available_slots(
            date=self.date,
            party_size=2
        )

        self.assertEqual(slots, [])
