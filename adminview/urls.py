from django.urls import path
from . import views

app_name = 'adminview'

urlpatterns = [
    path('reservations/', views.reservations_view, name='reservations'),
]
