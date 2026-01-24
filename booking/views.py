from django.http import JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from django.utils.timezone import localtime
from .forms import BookingForm
from .models import Booking


# def booking_page(request):
#     return render(request, 'booking/booking.html')


@login_required
def make_booking(request):
    user = request.user

    # Fetch the current user's bookings, ordered by start_time
    my_bookings = Booking.objects.filter(name=user).order_by('start_time')

    if request.method == "POST":
        form = BookingForm(
            request.POST,
            user=user
        )
        if form.is_valid():
            form.save()
            return redirect("booking:booking")
    else:
        form = BookingForm(
            request.GET or None,
            user=user
        )

    context = {
        "form": form,
        "my_bookings": my_bookings,
    }
    return render(request, "booking/booking.html", context)


def cancel_booking(request, booking_id):
    booking = get_object_or_404(Booking, id=booking_id, name=request.user)
    booking.status = 'CANCELLED'
    booking.save()
    return redirect("booking:booking")


# def edit_booking(request, booking_id):
#     booking = get_object_or_404(Booking, id=booking_id, user=request.user)

#     if request.method == "POST":
#         form = BookingForm(request.POST, instance=booking, user=request.user)
#         if form.is_valid():
#             form.save()
#             return redirect("make_booking")
#     else:
#         form = BookingForm(instance=booking, user=request.user)

#     return render(
#         request,
#         "edit_booking.html",
#         {"form": form, "booking": booking}
#     )


@staff_member_required(login_url="account_login")
def booking_calendar_data(request):
    """
    JSON endpoint consumed by FullCalendar.
    Returns bookings as calendar events.
    """

    bookings = (
        Booking.objects
        .select_related("table", "name")
        .exclude(status="CANCELLED")
    )

    events = []

    for booking in bookings:
        start = localtime(booking.start_time)
        end = localtime(booking.time_range.upper)

        events.append({
            "id": booking.id,
            "title": f"Table {booking.table} – {booking.name}",
            "start": start.isoformat(),
            "end": end.isoformat(),
            "extendedProps": {
                "reference": booking.reference,
                "status": booking.status,
                "allergies": booking.allergies,
            }
        })

    return JsonResponse(events, safe=False)
