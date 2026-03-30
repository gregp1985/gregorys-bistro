from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib import messages
from django.utils.dateparse import parse_datetime
from booking.models import Booking
from .forms import StaffBookingForm


@staff_member_required(login_url='account_login')
def reservations_view(request):
    """
    Staff-only Reservations page.
    This is the page linked from the main navigation.
    """
    return render(request, 'adminview/reservations.html')


@staff_member_required(login_url='account_login')
def cancellations_view(request):
    """
    Staff-only Cancellations page.
    This is the page linked from the main navigation.
    """
    bookings = Booking.objects.filter(status='CANCELLED')
    return render(request, 'adminview/cancellations.html', {
        'bookings': bookings
    })


@staff_member_required
def staff_delete_booking(request, booking_id):
    booking = get_object_or_404(Booking, id=booking_id)
    booking.delete()
    messages.success(request, f'Booking {booking.reference} has been deleted.')
    return redirect('adminview:cancellations')


@staff_member_required
def staff_booking(request, booking_id=None):
    booking = None
    if booking_id:
        booking = get_object_or_404(Booking, id=booking_id)  # ✅ Load instance

    if request.method == 'POST':
        form = StaffBookingForm(request.POST, instance=booking)
        if form.is_valid():
            new_booking = form.save(commit=False)
            slot = request.POST.get('slot')
            if slot:
                start_datetime = parse_datetime(slot)
                if start_datetime:
                    new_booking.start_time = start_datetime
            new_booking.name = form.cleaned_data['name']
            new_booking.save()
            messages.success(request, 'Booking saved successfully!')
            return redirect('adminview:reservations')
    else:
        form = StaffBookingForm(instance=booking)  # ✅ pre-filled for GET

    return render(
        request,
        'adminview/staff_booking.html',
        {
            'form': form,
            'booking': booking,
            'editing': True if booking else False
        }
    )
