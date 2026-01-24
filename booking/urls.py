from django.urls import path
from . import views

app_name = 'booking'

urlpatterns = [
    path(
        'admin/bookings/calendar-data/',
        views.booking_calendar_data,
        name='booking_calendar_data',
    ),
    path('booking/', views.make_booking, name='booking'),
]
