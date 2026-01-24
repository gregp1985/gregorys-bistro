import uuid
from django.db import models
from django.core.exceptions import ValidationError
from django.contrib.auth.models import User
from django.contrib.postgres.constraints import ExclusionConstraint
from django.contrib.postgres.fields import DateTimeRangeField
from django.contrib.postgres.indexes import GistIndex
from .utils import SLOT_DURATION


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
    start_time = models.DateTimeField()
    time_range = DateTimeRangeField(editable=False)
    status = models.CharField(
        max_length=10,
        choices=STATUS_CHOICES,
        default='BOOKED'
    )

    def clean(self):
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
        self.time_range = (
            self.start_time,
            self.start_time + SLOT_DURATION
        )

        # Generate reference if not set
        if not self.reference:
            # Simple approach: use UUID, truncated
            self.reference = str(uuid.uuid4()).replace("-", "")[:12].upper()

        super().save(*args, **kwargs)

    def __str__(self):
        return (
            f"{self.name} - {self.table} "
            f"@ {self.start_time.strftime('%Y-%m-%d %H:%M')} | "
            f"Ref: {self.reference} | Status: {self.status}"
        )
