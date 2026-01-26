from django.urls import path
from . import views

app_name = 'booking'

urlpatterns = [
    path(
        'admin/bookings/calendar-data/',
        views.booking_calendar_data,
        name='booking_calendar_data',
    ),
    path(
        'edit/<int:booking_id>/',
        views.edit_booking,
        name='edit_booking'
    ),
    path(
        'available-slots/',
        views.available_slots,
        name='available_slots'
    ),
    path(
        'cancel/<int:booking_id>/',
        views.cancel_booking,
        name='cancel_booking'
    ),
    path('', views.make_booking, name='booking'),
]
