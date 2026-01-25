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
        if date == now.date() and current <= now:
            current += INTERVAL
            continue
        free_tables = Table.objects.filter(
            seats__gte=party_size
        ).exclude(
            bookings__start_time__lt=current + SLOT_DURATION,
            bookings__start_time__gte=current,
        )

        if exclude_bookings:
            free_tables = free_tables.exclude(
                bookings__id=exclude_bookings.id
            )

        if free_tables.exists():
            slots.append((current, list(free_tables)))

        current += INTERVAL

    return slots
