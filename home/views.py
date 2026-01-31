from django.shortcuts import render, redirect
from django.contrib import messages
from django.core.mail import send_mail
from django.conf import settings
from .forms import ContactForm


def home_page(request):
    return render(request, 'home/index.html')


def contact_page(request):
    if request.method == "POST":
        form = ContactForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data["email"]
            message = form.cleaned_data["message"]

            send_mail(
                subject="New contact form submission",
                message=f"From: {email}\n\n{message}",
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=["gregorys.bistro.2026@gmail.com"],
            )

            messages.success(
                request,
                "Thanks! Your message has been sent. We'll be in touch soon."
            )
            return redirect("home:contact")
    else:
        form = ContactForm()

    return render(request, "home/contact.html", {"form": form})


def gallery_page(request):
    return render(request, 'home/gallery.html')


def menu_page(request):
    return render(request, 'home/menu.html')
