from django.http import JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from django.utils import timezone
from django.utils.timezone import localtime
from django.utils.dateparse import parse_date
from .forms import BookingForm
from .models import Booking
from .utils import get_available_slots


@login_required
def available_slots(request):
    date_str = request.GET.get('date')
    party_size = request.GET.get('party_size')
    exclude_id = request.GET.get('exclude')

    if not date_str or not party_size:
        return JsonResponse({'slots': []})

    date = parse_date(date_str)
    if not date:
        return JsonResponse({'slots': []})

    try:
        party_size = int(party_size)
    except (TypeError, ValueError):
        return JsonResponse({'slots': []})

    # Used when editing an existing booking
    exclude_bookings = None
    if exclude_id:
        exclude_bookings = Booking.objects.filter(
            id=exclude_id,
            name=request.user,
        )

    slots = get_available_slots(
        date=date,
        party_size=party_size,
        exclude_bookings=exclude_bookings,
    )

    data = [
        {
            'value': slot.isoformat(),
            'label': slot.strftime('%H:%M'),
        }
        for slot in slots
    ]

    return JsonResponse({'slots': data})


@login_required
def make_booking(request):
    now = timezone.now()

    upcoming_bookings = Booking.objects.filter(
        name=request.user,
        start_time__gte=now
        ).order_by('start_time')

    past_bookings = Booking.objects.filter(
        name=request.user,
        start_time__lt=now,
        ).order_by('-start_time')

    form = BookingForm(
        request.POST or None,
        user=request.user,
    )

    if request.method == 'POST' and form.is_valid():
        form.save()
        return redirect('booking:booking')

    return render(
        request,
        'booking/booking.html',
        {
            'form': form,
            'upcoming_bookings': upcoming_bookings,
            'past_bookings': past_bookings,
            'editing': False,
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


@login_required
def accountpage(request):
    return render(request, 'booking/accountpage.html')
