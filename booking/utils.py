from datetime import datetime
from django.utils import timezone
from django.db.models import Q
from .constants import SLOT_DURATION, INTERVAL


def get_available_slots(date, party_size=1, exclude_bookings=None):
    from .models import Table, OpeningHours

    weekday = date.weekday()

    try:
        opening = OpeningHours.objects.get(weekday=weekday)
    except OpeningHours.DoesNotExist:
        return []

    tz = timezone.get_current_timezone()
    now = timezone.now()

    start = timezone.make_aware(
        datetime.combine(date, opening.open_time),
        tz,
    )

    end = timezone.make_aware(
        datetime.combine(date, opening.close_time),
        tz,
    ) - SLOT_DURATION

    slots = []
    current = start

    while current <= end:
        # Don’t allow booking in the past
        if date == now.date() and current <= now:
            current += INTERVAL
            continue

        booking_end = current + SLOT_DURATION

        overlap_q = Q(
            bookings__time_range__overlap=(current, booking_end)
        )

        if exclude_bookings:
            overlap_q &= ~Q(bookings__in=exclude_bookings)

        available_tables = (
            Table.objects
            .filter(seats__gte=party_size)
            .exclude(overlap_q)
        )

        if available_tables.exists():
            slots.append(current)

        current += INTERVAL

    return slots
