from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.admin.views.decorators import staff_member_required
from booking.models import Booking
from booking.forms import BookingForm

@staff_member_required(login_url='account_login')
def reservations_view(request):
    """
    Staff-only Reservations page.
    This is the page linked from the main navigation.
    """
    return render(request, 'adminview/reservations.html')


@staff_member_required
def staff_edit_booking(request, booking_id):
    booking = get_object_or_404(Booking, id=booking_id)

    if request.method == 'POST':
        form = BookingForm(
            request.POST,
            instance=booking,
            user=booking.name,  # booking owner
        )
        if form.is_valid():
            form.save()
            return redirect('adminview:reservations')
    else:
        form = BookingForm(
            instance=booking,
            user=booking.name,
        )

    return render(
        request,
        'adminview/staff_edit_booking.html',
        {
            'form': form,
            'booking': booking,
        }
    )
