from django.conf import settings
from django.contrib import admin, messages
from django.template.loader import render_to_string
from django.core.mail import send_mail
from .models import Booking, OpeningHours, Table
from .forms import BookingAdminForm

admin.site.register(OpeningHours)
admin.site.register(Table)


@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    """
    Lists fields for display in admin, fields for search,
    field filters and fields to prepopulate.
    """
    list_display = (
        'reference',
        'start_time',
        'name',
        'party_size',
        'status',
    )

    list_filter = (
        'start_time',
        'name',
    )

    search_fields = (
        'reference',
        'name__username',
        'name__email',
    )

    date_hierarchy = 'start_time'

    form = BookingAdminForm

    def save_model(self, request, obj, form, change):
        previous_status = None
        if change and obj.pk:
            try:
                previous_status = (
                    Booking.objects
                    .only('status')
                    .get(pk=obj.pk)
                    .status
                )
            except Booking.DoesNotExist:
                previous_status = None

        super().save_model(request, obj, form, change)

        if (
            change
            and previous_status != 'CANCELLED'
            and obj.status == 'CANCELLED'
            and obj.name.email
        ):

            reason = form.cleaned_data.get('cancellation_reason')

            context = {
                'user': obj.name,
                'booking': obj,
                'reason': reason,
            }

            message = render_to_string(
                'account/email/cancellation_notification.txt',
                context,
            )

            send_mail(
                subject=(
                    'Gregorys Bistro: '
                    f'Booking cancelled - Ref {obj.reference}'
                ),
                message=message,
                from_email=getattr(settings, 'DEFAULT_FROM_EMAIL', None),
                recipient_list=[obj.name.email],
                fail_silently=False,
            )

            messages.success(
                request,
                f'Cancellation email sent to {obj.name.email}.',
            )
