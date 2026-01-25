import uuid
from django.db import models
from django.core.exceptions import ValidationError
from django.contrib.auth.models import User
from django.contrib.postgres.constraints import ExclusionConstraint
from django.contrib.postgres.fields import DateTimeRangeField
from django.contrib.postgres.indexes import GistIndex
from django.utils import timezone
from django.utils.dateparse import parse_datetime
from .constants import SLOT_DURATION


class Table(models.Model):
    number = models.IntegerField()
    seats = models.PositiveIntegerField()

    def __str__(self):
        return f"Table No. {self.number} ({self.seats} seats)"


class OpeningHours(models.Model):
    WEEKDAYS = [
        (0, "Monday"),
        (1, "Tuesday"),
        (2, "Wednesday"),
        (3, "Thursday"),
        (4, "Friday"),
        (5, "Saturday"),
        (6, "Sunday"),
    ]

    weekday = models.IntegerField(choices=WEEKDAYS)
    open_time = models.TimeField()
    close_time = models.TimeField()

    class Meta:
        unique_together = ("weekday",)

    def __str__(self):
        return (
            f"{self.get_weekday_display()}: "
            f"{self.open_time}-{self.close_time}"
        )


class Booking(models.Model):
    STATUS_CHOICES = [
        ('BOOKED', 'Booked'),
        ('CANCELLED', 'Cancelled'),
    ]

    table = models.ForeignKey(
        "Table",
        related_name="bookings",
        on_delete=models.CASCADE
    )
    name = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="bookings"
    )
    reference = models.CharField(max_length=12, unique=True, editable=False)
    allergies = models.TextField(blank=True)
    party_size = models.PositiveSmallIntegerField()
    start_time = models.DateTimeField()
    time_range = DateTimeRangeField(editable=False)
    status = models.CharField(
        max_length=10,
        choices=STATUS_CHOICES,
        default='BOOKED'
    )

    def clean(self):
        if not self.start_time:
            return

        if isinstance(self.start_time, str):
            self.start_time = parse_datetime(self.start_time)

        if not self.start_time:
            raise ValidationError("Invalid booking time.")

        weekday = self.start_time.weekday()

        try:
            opening = OpeningHours.objects.get(weekday=weekday)
        except OpeningHours.DoesNotExist:
            raise ValidationError("The restaurant is closed on this day.")

        start = self.start_time.time()
        end = (self.start_time + SLOT_DURATION).time()

        if start < opening.open_time or end > opening.close_time:
            raise ValidationError(
                "Booking time is outside opening hours."
            )

    class Meta:
        constraints = [
            ExclusionConstraint(
                name="prevent_table_double_booking",
                expressions=[
                    ("table", "="),
                    ("time_range", "&&"),
                ],
            ),
        ]
        indexes = [
            GistIndex(fields=["time_range"]),
        ]

    def save(self, *args, **kwargs):
        if self.start_time and timezone.is_naive(self.start_time):
            self.start_time = timezone.make_aware(
                self.start_time,
                timezone.get_current_timezone(),
            )

        self.time_range = (
            self.start_time,
            self.start_time + SLOT_DURATION
        )

        # Generate reference
        if not self.reference:
            self.reference = str(uuid.uuid4()).replace("-", "")[:12].upper()

        super().save(*args, **kwargs)

    def __str__(self):
        return (
            f"{self.name} - {self.table} "
            f"@ {self.start_time.strftime('%Y-%m-%d %H:%M')} | "
            f"Ref: {self.reference} | Status: {self.status}"
        )
