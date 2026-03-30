from django.urls import path
from . import views

app_name = 'adminview'

urlpatterns = [
    path(
        'staff/cancel/<booking_ref>/',
        views.staff_cancel_booking,
        name='staff_cancel_booking'
    ),
    path(
        'cancellations/delete/<int:booking_id>/',
        views.staff_delete_booking,
        name='staff_delete_booking',
    ),
    path('cancellations/', views.cancellations_view, name='cancellations'),
    path('reservations/', views.reservations_view, name='reservations'),
    path(
        'reservations/edit/<int:booking_id>/',
        views.staff_booking,
        name='staff_booking_edit',
    ),
    path('staff_booking/', views.staff_booking, name='staff_booking'),
]
