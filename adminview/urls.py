from django.urls import path
from . import views

urlpatterns = [
    path('reservations/', views.reservation_page, name="reservations"),
]
