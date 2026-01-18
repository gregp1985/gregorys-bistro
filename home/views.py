from django.shortcuts import render

# Create your views here.


def home_page(request):
    return render(request, 'home/index.html')


def contact_page(request):
    return render(request, 'home/contact.html')


def gallery_page(request):
    return render(request, 'home/gallery.html')


def menu_page(request):
    return render(request, 'home/menu.html')
