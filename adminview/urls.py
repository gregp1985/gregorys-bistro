from django.urls import path
from . import views

app_name = 'adminview'

urlpatterns = [
    path(
        'cancellations/delete/<int:booking_id>/',
        views.staff_delete_booking,
        name='staff_delete_booking',
    ),
    path('cancellations/', views.cancellations_view, name='cancellations'),
    path('reservations/', views.reservations_view, name='reservations'),
    path(
        'reservations/edit/<int:booking_id>/',
        views.staff_edit_booking,
        name='staff_edit_booking',
    ),
]
