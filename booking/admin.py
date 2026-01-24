from django.contrib import admin
from .models import Booking, OpeningHours, Table

admin.site.register(Booking)
admin.site.register(OpeningHours)
admin.site.register(Table)
