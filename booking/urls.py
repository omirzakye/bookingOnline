from django.urls import path
from .views import *

urlpatterns = [
    path('', IndexView.as_view(), name='home'),
    path('login/', LoginUserView.as_view(), name='login'),
    path('register/', RegisterView.as_view(), name='register'),
    path('logout/', logout_user, name='logout'),
    path('search/', search_rest_by_name, name='search_rest_by_name'),
    path('search/<str:text>/', search_success, name='search_success'),
    path('restaurant/<int:rest_id>/', restaurant, name="restaurant"),
    path('restaurant/<int:idd>/reserve/$', reserve, name='table-reserve'),
    path('reservations', reservations, name='reservations')
]