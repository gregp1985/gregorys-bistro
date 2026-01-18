from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .forms import BookingForm
from .models import Booking


def booking_page(request):
    return render(request, 'booking/booking.html')


@login_required
def make_booking(request):
    user = request.user

    # Fetch the current user's bookings, ordered by start_time
    my_bookings = Booking.objects.filter(user=user).order_by('start_time')

    if request.method == "POST":
        form = BookingForm(request.POST, user=user)
        if form.is_valid():
            form.save()
            return redirect("booking_success")
    else:
        form = BookingForm(user=user)

    context = {
        "form": form,
        "my_bookings": my_bookings,
    }
    return render(request, "booking.html", context)
