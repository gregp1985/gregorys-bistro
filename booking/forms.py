from datetime import datetime
from django import forms
from django.utils import timezone
from django.utils.dateparse import parse_date
from django.core.exceptions import ValidationError
from .models import Booking, Table
from .utils import get_available_slots
from .constants import SLOT_DURATION


class BookingForm(forms.ModelForm):
    date = forms.DateField(
        widget=forms.DateInput(
            attrs={
                'type': 'date',
                'min': timezone.localdate().isoformat(),
            }
        )
    )

    slot = forms.ChoiceField(
        label='Time',
        choices=[],
        required=True,
    )

    class Meta:
        model = Booking
        exclude = (
            'start_time',
            'table',
            'name',
            'status',
        )
        widgets = {
            'allergies': forms.Textarea(attrs={'rows': 2})
        }

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        self.instance = kwargs.get('instance')
        super().__init__(*args, **kwargs)

        # Let AJAX populate on GET
        if not self.is_bound:
            return

        selected_date = self.data.get('date')
        party_size = self.data.get('party_size')

        if not selected_date or not party_size:
            return

        try:
            selected_date = parse_date(selected_date)
            party_size = int(party_size)
        except (TypeError, ValueError):
            return

        if not selected_date:
            return

        # Used when editing an existing booking
        exclude_bookings = None
        if self.instance and self.instance.pk:
            exclude_bookings = Booking.objects.filter(pk=self.instance.pk)

        slots = get_available_slots(
            date=selected_date,
            party_size=party_size,
            exclude_bookings=exclude_bookings,
        )

        if self.instance and self.instance.pk and self.instance.start_time:
            slots = list(slots)
            if self.instance.start_time not in slots:
                slots.append(self.instance.start_time)

        slots = sorted(slots)

        self.fields['slot'].choices = [
            (slot.isoformat(), slot.strftime('%H:%M'))
            for slot in slots
        ]

    def clean(self):
        cleaned_data = super().clean()
        slot_value = cleaned_data.get('slot')

        if not slot_value:
            return cleaned_data

        try:
            start_dt = datetime.fromisoformat(slot_value)

            if timezone.is_naive(start_dt):
                start_dt = timezone.make_aware(start_dt)

        except Exception as e:
            raise ValidationError('Invalid time slot selected.')

        cleaned_data['start_time'] = start_dt

        return cleaned_data

    def save(self, commit=True):
        if "start_time" not in self.cleaned_data:
            raise forms.ValidationError("Please select a valid booking time.")

        booking = super().save(commit=False)

        booking.start_time = self.cleaned_data["start_time"]
        booking.party_size = self.cleaned_data["party_size"]
        booking.name = self.user

        start = booking.start_time
        end = booking.start_time + SLOT_DURATION

        table_qs = Table.objects.filter(seats__gte=booking.party_size)

        # Bookings that would conflict with this slot (ignore CANCELLED)
        conflict_bookings = Booking.objects.filter(
            status="BOOKED",
            time_range__overlap=(start, end),
        )

        # When editing, exclude the booking itself from the conflict check
        if booking.pk:
            conflict_bookings = conflict_bookings.exclude(pk=booking.pk)

        # Exclude any table that has a conflicting booking
        table_qs = table_qs.exclude(bookings__in=conflict_bookings)

        # Pick the smallest suitable table
        booking.table = table_qs.order_by("seats").first()

        if booking.table_id is None:
            raise forms.ValidationError(
                "That time is no longer available. Please choose another."
            )

        if commit:
            booking.save()

        return booking


class BookingAdminForm(forms.ModelForm):
    cancellation_reason = forms.CharField(
        required=False,
        widget=forms.Textarea(attrs={"rows": 3}),
        help_text="Optional reason sent to the customer",
        label="Cancellation reason",
    )

    class Meta:
        model = Booking
        fields = "__all__"

    def clean(self):
        cleaned_data = super().clean()
        status = cleaned_data.get("status")
        reason = cleaned_data.get("cancellation_reason")

        if status == "CANCELLED" and not reason:
            raise forms.ValidationError(
                "Please provide a cancellation reason."
            )

        return cleaned_data
