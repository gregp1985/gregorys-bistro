from django import forms
from django.utils import timezone
from django.utils.dateparse import parse_datetime
from datetime import datetime
from .constants import SLOT_DURATION
from .models import Booking, Table
from .utils import get_available_slots


class BookingForm(forms.ModelForm):
    party_size = forms.IntegerField(
        min_value=1,
        max_value=12,
        initial=0,
        widget=forms.NumberInput(attrs={"onchange": "this.form.submit()"})
    )

    date = forms.DateField(
        widget=forms.DateInput(
            attrs={"type": "date", "onchange": "this.form.submit()"}
        )
    )

    slot = forms.ChoiceField(
        label="Time",
        choices=[],
        required=False
    )

    class Meta:
        model = Booking
        fields = ["date", "party_size", "allergies"]
        widgets = {
            "allergies": forms.Textarea(
                attrs={
                    "rows": 2,
                }
            )
        }

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop("user", None)
        super().__init__(*args, **kwargs)

        data = self.data or {}
        selected_date = data.get("date")
        party_size = data.get("party_size")

        if not selected_date or not party_size:
            return

        try:
            selected_date = datetime.fromisoformat(selected_date).date()
            party_size = int(party_size)
        except Exception:
            return

        slots = get_available_slots(selected_date, party_size)

        choices = []
        for slot_time, tables in slots:
            table = tables[0]  # safe: availability already checked
            value = f"{slot_time.isoformat()}|{table.pk}"
            label = (
                f"{slot_time.strftime('%H:%M')} – "
                f"{(slot_time + SLOT_DURATION).strftime('%H:%M')}"
            )
            choices.append((value, label))

        self.fields["slot"].choices = choices

    def clean(self):
        cleaned_data = super().clean()
        slot_value = cleaned_data.get("slot")

        if not slot_value:
            return cleaned_data

        try:
            start_iso, table_pk = slot_value.split("|")
            start_dt = parse_datetime(start_iso)

            if start_dt is None:
                raise ValueError

            if timezone.is_naive(start_dt):
                start_dt = timezone.make_aware(start_dt)

            cleaned_data["start_time"] = start_dt
            cleaned_data["table"] = Table.objects.get(pk=table_pk)

        except Exception:
            raise forms.ValidationError("Invalid booking slot selected.")

        return cleaned_data

    def save(self, commit=True):
        booking = super().save(commit=False)
        booking.start_time = self.cleaned_data["start_time"]
        booking.table = self.cleaned_data["table"]
        booking.name = self.user

        if commit:
            booking.save()

        return booking
