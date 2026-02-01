from datetime import time
from django.test import TestCase
from django.utils import timezone
from booking.models import Table, OpeningHours
from booking.utils import get_available_slots


class GetAvailableSlotsTests(TestCase):

    def setUp(self):
        # Opening hours: 11:00–23:00 for all days
        for weekday in range(7):
            OpeningHours.objects.create(
                weekday=weekday,
                open_time=time(11, 0),
                close_time=time(23, 0),
            )

        self.table_2 = Table.objects.create(number=1, seats=2)
        self.table_4 = Table.objects.create(number=2, seats=4)

        self.today = timezone.localdate()

    def test_returns_slots_within_opening_hours(self):
        slots = get_available_slots(self.today, party_size=2)

        self.assertTrue(slots)
        self.assertGreaterEqual(slots[0].time(), time(11, 0))
        