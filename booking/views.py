from django.shortcuts import render

# Create your views here.


def booking_page(request):
    return render(request, 'booking/booking.html')
