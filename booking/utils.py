from datetime import datetime
from django.utils import timezone
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

        candidate_end = current + SLOT_DURATION

        available_tables = (
            Table.objects
            .filter(seats__gte=party_size)
            .exclude(
                bookings__time_range__overlap=(current, candidate_end)
            )
        )

        # Used when editing an existing booking
        if exclude_bookings:
            available_tables = available_tables.exclude(
                bookings__in=exclude_bookings
            )

        if available_tables.exists():
            slots.append(current)

        current += INTERVAL

    return slots
