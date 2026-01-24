from django.urls import path
from . import views

app_name = 'home'

urlpatterns = [
    path('contact/', views.contact_page, name='contact'),
    path('gallery/', views.gallery_page, name='gallery'),
    path('menu/', views.menu_page, name='menu'),
    path('home/', views.menu_page, name='home'),
    path('', views.home_page, name='home'),
]
