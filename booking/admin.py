from django.contrib import admin
from .models import Booking, OpeningHours, Table


admin.site.register(OpeningHours)
admin.site.register(Table)


@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    """
    Lists fields for display in admin, fields for search,
    field filters and fields to prepopulate.
    """
    list_display = (
        "reference",
        "start_time",
        "name",
        "party_size",
        "status",
    )

    list_filter = (
        "start_time",
        "name",
    )

    search_fields = (
        "reference",
        "name__username",
        "name__email",
    )

    date_hierarchy = "start_time"
