from django.contrib import messages
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import CreateView, ListView, DetailView
from . import models
from booking.forms import CustomRegisterUserForm, CustomLoginUserForm
from booking.models import Restaurants, CustomUser, Bookings
import datetime
from datetime import datetime, date, timedelta


class IndexView(ListView):
    template_name = "booking/index.html"
    context_object_name = "all_restaurants"
    queryset = Restaurants.objects.all();

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # context['popular_items'] = Item.objects.filter(num_of_views__gt=0).order_by('-num_of_views')[:4]
        return context


# JavaSCript optimize
def search_rest_by_name(request):
    if request.method == "POST" and len(request.POST.get("search_field")) > 0:
        searching_text = request.POST.get("search_field")
        return redirect("search_success", text=searching_text)
    else:
        return render(request, "booking/index.html",
                      {"all_restaurants": "No results found"})


def search_success(request, text):
    if len(text) > 0:
        search_res = Restaurants.objects.filter(name__icontains=text)
        return render(request, "booking/index.html", {"all_restaurants": search_res, "empty_res": "No results found"})


def restaurant(request, rest_id):
    rt = models.Restaurants.objects.filter(id=rest_id).first()  # restaurant
    context = {
        'name': rt.name,
        'idd': rt.id,
        'restaurant': rt,
        'available': rt.total_seats - rt.busy_seats,
        'pic': rt.photos,
        'open-time': rt.open_time,
        'close-time': rt.close_time
    }
    return render(request, 'booking/restaurant.html', context)


@login_required
def reserve(request, idd):
    rt = models.Restaurants.objects.filter(id=idd).first()  # restaurant
    rdate = request.GET.get('date')
    size = int(request.GET.get('size'))
    rtime = datetime.strptime(request.GET.get('time'), '%H:%M').time()
    context = {
        'name': rt.name,
        'idd': rt.id,
        'restaurant': rt,
        'total': rt.total_seats,
        'pic': rt.photos,
        'open-time': rt.open_time,
        'close-time': rt.close_time,
        'date': rdate,
        'time': rtime
    }

    if request.method == 'POST':
        firstname = request.POST.get('firstname')
        surname = request.POST.get('surname')
        phone = request.POST.get('phone')
        email = request.POST.get('email')
        specialRequest = request.POST.get('specialRequest')
        context.update({
            'firstname': firstname,
            'surname': surname,
            'phone': phone,
            'email': email,
            'specialRequest': specialRequest,
        })
        endTime = (datetime.combine(date.min, rtime) + timedelta(hours=3)).time()
        reservation = models.Bookings(number_of_people=size, reserve_date=rdate, status=True, restaurant_id=rt.id,
                                      user_id=request.user.id,
                                      reserve_time_end=endTime,
                                      reserve_time_start=rtime,
                                      reserverFname=firstname,
                                      reserverLname=surname,
                                      email=email,
                                      phone=phone,
                                      specialRequest=specialRequest)
        reservation.save()
        rt.busy_seats += size
        rt.save()
        messages.success(request, 'You have successfully reserved a table. Please be on time!')
        return redirect('reservations')

    if not ifAvailable(rt.id, rtime, size):
        context.update({
            'decline': "No available seats for this hour!"
        })
        return render(request, 'booking/restaurant.html', context)
    else:
        return render(request, 'booking/reserve.html', context)


class RegisterView(CreateView):
    form_class = CustomRegisterUserForm
    template_name = 'registrations/registration.html'
    success_url = reverse_lazy('home')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Register'
        return context

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return redirect('home')


class LoginUserView(LoginView):
    form_class = CustomLoginUserForm
    template_name = 'registrations/login.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Log in'
        return context


@login_required
def logout_user(request):
    logout(request)
    return redirect('login')


@login_required
def reservations(request):
    context = {
        'title': 'My reservations',
        'reservations': models.Bookings.objects.filter(user=request.user),
        'today': date.today()
    }
    return render(request, 'booking/reservations.html', context)


@login_required()
def edit_Reservation(request, id):
    booking = models.Bookings.objects.filter(id=id).first()
    numOfPeople = request.POST.get('number_of_people')
    time = request.POST.get('time_start')
    ifAvailable()


def ifAvailable(rest_id, time_start, numOfPeople):
    bookings = models.Bookings.objects.filter(restaurant=rest_id).all()
    restaurant = models.Restaurants.objects.filter(id=rest_id).first()
    timeMinusThree = datetime.combine(date.min, time_start) - datetime.combine(date.min, datetime.strptime('03:00',
                                                                                                           '%H:%M').time())
    quantity = bookings.filter(reserve_time_start__gt=str(timeMinusThree), reserve_time_end__gt=time_start).values_list(
        'number_of_people', flat=True)
    totalQuantity = 0
    for q in quantity:
        totalQuantity += q

    if restaurant.open_time < time_start < restaurant.close_time:
        if restaurant.total_seats - totalQuantity >= numOfPeople:
            return True
    else:
        return False

