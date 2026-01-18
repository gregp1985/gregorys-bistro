from datetime import datetime, timedelta
from .models import Table, OpeningHours

SLOT_DURATION = timedelta(hours=1, minutes=30)
INTERVAL = timedelta(minutes=15)


def get_available_slots(date, party_size=1):
    weekday = date.weekday()
    try:
        opening = OpeningHours.objects.get(weekday=weekday)
    except OpeningHours.DoesNotExist:
        return []  # closed that day

    start = datetime.combine(date, opening.open_time)
    end = datetime.combine(date, opening.close_time) - SLOT_DURATION

    slots = []
    current = start
    while current <= end:
        # Tables available for this slot
        free_tables = Table.objects.filter(seats__gte=party_size).exclude(
            bookings__time_range__overlap=(current, current + SLOT_DURATION)
        )
        if free_tables.exists():
            slots.append((current, list(free_tables)))
        current += INTERVAL
    return slots