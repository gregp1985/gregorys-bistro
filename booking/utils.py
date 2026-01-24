from datetime import datetime, timedelta


SLOT_DURATION = timedelta(hours=1, minutes=30)
INTERVAL = timedelta(minutes=15)


def get_available_slots(date, party_size=1):
    from .models import Table, OpeningHours

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
            bookings__start_time__lt=current + SLOT_DURATION,
            bookings__start_time__gte=current
        )
        if free_tables.exists():
            slots.append((current, list(free_tables)))
        current += INTERVAL
    return slots
