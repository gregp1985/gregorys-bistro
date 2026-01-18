from django.urls import path
from . import views

urlpatterns = [
    path('contact/', views.contact_page, name="contact"),
    path('gallery/', views.gallery_page, name="gallery"),
    path('menu/', views.menu_page, name="menu"),
    path('', views.home_page, name="home"),
]
