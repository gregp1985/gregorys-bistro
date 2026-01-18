from django import forms
from .models import Booking, Table
from .utils import get_available_slots, SLOT_DURATION


class BookingForm(forms.ModelForm):
    date = forms.DateField(
        widget=forms.SelectDateWidget,
        label="Booking Date"
    )

    class Meta:
        model = Booking
        fields = ["date", "start_time", "table", "reference", "allergies"]

    def __init__(self, *args, **kwargs):
        # Expect logged-in user and optional party_size in kwargs
        self.user = kwargs.pop("user", None)
        self.party_size = kwargs.pop("party_size", 1)
        super().__init__(*args, **kwargs)

        # Only show start_time and table after date is selected
        if "date" in self.data:
            try:
                selected_date = forms.fields.datetime.date.fromisoformat(self.data["date"])
            except Exception:
                selected_date = None
        else:
            selected_date = None

        if selected_date:
            # Generate slots for the selected date
            slots = get_available_slots(selected_date, self.party_size)
            choices = []

            for slot_time, tables in slots:
                for table in tables:
                    choices.append((
                        f"{slot_time.isoformat()}_{table.pk}",
                        f"{slot_time.strftime('%H:%M')} - {(slot_time + SLOT_DURATION).strftime('%H:%M')} | {table}"
                    ))

            self.fields["start_time"].widget = forms.Select(choices=choices)
            self.fields["table"].widget = forms.HiddenInput()  # table selected via slot value
        else:
            self.fields["start_time"].widget = forms.Select(choices=[])

    def clean(self):
        cleaned_data = super().clean()
        slot_value = cleaned_data.get("start_time")
        if slot_value:
            try:
                start_iso, table_pk = slot_value.split("_")
                cleaned_data["start_time"] = start_iso
                cleaned_data["table"] = Table.objects.get(pk=table_pk)
            except Exception:
                raise forms.ValidationError("Invalid slot selection.")
        return cleaned_data

    def save(self, commit=True):
        booking = super().save(commit=False)
        if self.user:
            booking.user = self.user
        if commit:
            booking.save()
        return booking
