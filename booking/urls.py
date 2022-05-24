from django.urls import path
from .views import *

urlpatterns = [
    path('', IndexView.as_view(), name='home'),
    path('search/', search_rest_by_name, name='search_rest_by_name'),
    path('search/<str:text>/', search_success, name='search_success'),
    path('restaurant/<int:rest_id>/', restaurant, name="restaurant"),
    path('restaurant/<int:idd>/reserve/$', reserve, name='table-reserve'),
    path('reservations', reservations, name='reservations'),
    path('reservations/<int:id>', edit_Res, name='edit_res'),
    path('reservations/<int:id>/edit', edit_Reservation, name='edit_reservation'),
    path('reservations/<int:id>/delete', delete_Reservation, name='delete_res'),
    path('reservations/<int:id>/order', order, name='add_order'),
    path('add/', addToOrder, name='addToOrder'),
    path('checkout/<int:booking_id>', checkOut, name='checkout'),
    path('process_order/', processOrder, name="process_order"),
    path('aboutus/', aboutUs, name="about_us")
]