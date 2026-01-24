from django.shortcuts import render
from django.contrib.admin.views.decorators import staff_member_required



@staff_member_required(login_url="account_login")
def reservations_view(request):
    """
    Staff-only Reservations page.
    This is the page linked from the main navigation.
    """
    return render(request, "adminview/reservations.html")
