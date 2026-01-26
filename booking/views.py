from django.http import JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from django.utils.timezone import localtime
from datetime import datetime
from .forms import BookingForm
from .models import Booking
from .constants import SLOT_DURATION
from .utils import get_available_slots


@login_required
def available_slots(request):
    date = request.GET.get('date')
    party_size = request.GET.get('party_size')

    if not date or not party_size:
        return JsonResponse({'slots': []})

    try:
        date = datetime.fromisoformat(date).date()
        party_size = int(party_size)
    except ValueError:
        return JsonResponse({'slots': []})

    slots = get_available_slots(date, party_size)

    data = []
    for slot_time, tables in slots:
        table = tables[0]
        data.append({
            'value': f'{slot_time.isoformat()}|{table.pk}',
            'label': (
                f'{slot_time.strftime("%H:%M")}'
            )
        })

    return JsonResponse({'slots': data})


@login_required
def make_booking(request):
    my_bookings = Booking.objects.filter(
        name=request.user).order_by('start_time')

    if request.method == 'POST':
        form = BookingForm(
            request.POST,
            user=request.user,
        )
        if form.is_valid():
            form.save()
            return redirect('booking:booking')
    else:
        form = BookingForm(user=request.user)

    return render(
        request,
        'booking/booking.html',
        {
            'form': form,
            'my_bookings': my_bookings,
        }
    )


def cancel_booking(request, booking_id):
    booking = get_object_or_404(Booking, id=booking_id, name=request.user)
    booking.status = 'CANCELLED'
    booking.save()
    return redirect('booking:booking')


@staff_member_required(login_url='account_login')
def booking_calendar_data(request):
    """
    JSON endpoint consumed by FullCalendar.
    Returns bookings as calendar events.
    """

    bookings = (
        Booking.objects
        .select_related('table', 'name')
        .exclude(status='CANCELLED')
    )

    events = []

    for booking in bookings:
        start = localtime(booking.start_time)
        end = localtime(booking.time_range.upper)

        events.append({
            'id': booking.id,
            'title': f'Table {booking.table} - {booking.name}',
            'start': start.isoformat(),
            'end': end.isoformat(),
            'extendedProps': {
                'reference': booking.reference,
                'status': booking.status,
                'allergies': booking.allergies,
            }
        })

    return JsonResponse(events, safe=False)


@login_required
def edit_booking(request, booking_id):
    booking = get_object_or_404(
        Booking,
        id=booking_id,
        name=request.user,
        status='BOOKED',
    )

    if request.method == 'POST':
        form = BookingForm(
            request.POST,
            instance=booking,
            user=request.user,
        )
        if form.is_valid():
            form.save()
            return redirect('booking:booking')
    else:
        form = BookingForm(
            instance=booking,
            user=request.user,
        )

    return render(
        request,
        'booking/booking.html',
        {
            'form': form,
            'my_bookings': Booking.objects.filter(name=request.user),
            'editing': True,
        }
    )
