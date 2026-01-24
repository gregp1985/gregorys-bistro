from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('accounts/', include('allauth.urls')),
    path('admin/', admin.site.urls),
    path('', include('booking.urls'), name='booking-urls'),
    path('', include('adminview.urls'), name='adminview-urls'),
    path('', include('home.urls'), name='home-urls'),
]
