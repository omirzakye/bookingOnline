import json
from django.contrib import messages
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView
from django.core.mail import send_mail
from django.http import JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import CreateView, ListView, DetailView

from BookingRest import settings
from . import models
from booking.forms import CustomRegisterUserForm, CustomLoginUserForm
from booking.models import Restaurants, CustomUser, Bookings, Items, Orders, OrderItem
import datetime
from datetime import datetime, date, timedelta


class IndexView(ListView):
    template_name = "booking/index.html"
    context_object_name = "all_restaurants"
    queryset = Restaurants.objects.all()

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
    menu = models.Menu.objects.filter(restaurant_id=rest_id).first()
    items = models.Items.objects.filter(menu_id=menu.id).all().order_by('type')
    context = {
        'name': rt.name,
        'idd': rt.id,
        'restaurant': rt,
        'available': rt.total_seats - rt.busy_seats,
        'pic': rt.photo,
        'open-time': rt.open_time,
        'close-time': rt.close_time,
        'menu': items
    }
    return render(request, 'booking/restaurant.html', context)


@login_required
def reserve(request, idd):
    rt = models.Restaurants.objects.filter(id=idd).first()  # restaurant
    rdate = request.POST.get('date')
    size = int(request.POST.get('size'))
    rtime = datetime.strptime(request.POST.get('time'), '%H:%M').time()
    context = {
        'name': rt.name,
        'idd': rt.id,
        'restaurant': rt,
        'total': rt.total_seats,
        'pic': rt.photo,
        'open-time': rt.open_time,
        'close-time': rt.close_time,
        'date': rdate,
        'time': rtime
    }

    if not ifAvailable(rt.id, rtime, size):
        context.update({
            'decline': "No available seats for this hour!"
        })
        return render(request, 'booking/restaurant.html', context)
    else:
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
            # messaging to gmail section
            subject = 'Table Reservation'
            msg = 'You have successfully reserved a table at ' + rt.name + ' for ' + str(size) + ' people at ' + str(rtime) + '. Please be on time!'
            recipient = email
            send_mail(subject,
                      msg, settings.EMAIL_HOST_USER, [recipient], fail_silently=False)
            return redirect('reservations')


@login_required
def reservations(request):
    context = {
        'title': 'My reservations',
        'reservations': models.Bookings.objects.filter(user=request.user),
        'today': date.today()
    }
    return render(request, 'booking/reservations.html', context)


@login_required()
def delete_Reservation(request, id):
    booking = models.Bookings.objects.filter(id=id).first()
    booking.delete()
    messages.info(request, "Reservation successfully deleted!")
    return redirect('reservations')


@login_required()
def edit_Res(request, id):
    bk = models.Bookings.objects.filter(id=id).first()  # restaurant
    menu = models.Menu.objects.filter(restaurant_id=bk.restaurant_id).first()
    items = models.Items.objects.filter(menu_id=menu.id).all().order_by('type')
    context = {
        'name': bk.restaurant.name,
        'id': bk.id,
        'restaurant': bk.restaurant,
        'available': bk.restaurant.total_seats - bk.restaurant.busy_seats,
        'open-time': bk.restaurant.open_time,
        'close-time': bk.restaurant.close_time,
        'menu': items
    }
    # messaging to gmail section
    subject = 'Table Reservation'
    msg = 'You have successfully reserved a table at ' + bk.restaurant.name + ' for ' + str(bk.number_of_people) + ' people at ' + str(bk.reserve_time_start) + '. Please be on time!'
    recipient = bk.email
    send_mail(subject,
              msg, settings.EMAIL_HOST_USER, [recipient], fail_silently=False)
    return render(request, 'booking/edit_reservations.html', context)


@login_required()
def edit_Reservation(request, id):
    booking = models.Bookings.objects.filter(id=id).first()
    numOfPeople = int(request.POST.get('size'))
    time_start = datetime.strptime(request.POST.get('time'), '%H:%M').time()
    if ifAvailable(booking.restaurant_id, time_start, numOfPeople):
        booking.reserve_time_start = time_start
        booking.reserve_time_end = (datetime.combine(date.min, time_start) + timedelta(hours=3)).time()
        booking.number_of_people = numOfPeople
        booking.save()
        messages.info(request, "Reservation successfully updated!")
        return redirect('reservations')
    else:
        messages.error(request, "The are no free seats at this time, try again!")
        return redirect('reservations')


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


@login_required()
def order(request, id):
    booking = models.Bookings.objects.filter(id=id).first()  # restaurant
    rt = booking.restaurant
    ordr = models.Orders.objects.filter(booking_id=booking.id, complete=False).first()
    ordrItems = models.OrderItem.objects.filter(order=ordr).order_by('product_id')
    menu = models.Menu.objects.filter(restaurant_id=rt.id).first()
    items = models.Items.objects.filter(menu_id=menu.id).all().order_by('type')
    context = {
        'rest_name': rt.name,
        'rest_id': rt.id,
        'restaurant': rt,
        'available': rt.total_seats - rt.busy_seats,
        'pic': rt.photo,
        'open-time': rt.open_time,
        'close-time': rt.close_time,
        'menu': items,
        'booking_id': booking.id,
        'ordered_items': ordrItems
    }
    return render(request, 'booking/add_order.html', context)


@login_required()
def addToOrder(request):
    data = json.loads(request.body)
    productId = data['productId']
    action = data['action']
    bookingId = data['bookingId']
    print('Action:', action)
    print('Product:', productId)
    customer = request.user
    product = Items.objects.get(id=productId)
    print('Product:', product.id, ' ', product.name)
    bk = models.Bookings.objects.filter(id=bookingId).first()

    order, created = Orders.objects.get_or_create(booking=bk, customer=customer, complete=False)
    orderItem, created = OrderItem.objects.get_or_create(order=order, product=product)

    if action == 'add':
        orderItem.quantity = (orderItem.quantity + 1)
    elif action == 'remove':
        orderItem.quantity = (orderItem.quantity - 1)

    orderItem.save()

    if orderItem.quantity <= 0:
        orderItem.delete()

    return JsonResponse('Item was added', safe=False)


def checkOut(request, booking_id):
    if request.user.is_authenticated:
        bk = models.Bookings.objects.filter(id=booking_id).first()
        customer = request.user
        order, created = Orders.objects.get_or_create(booking=bk, customer=customer, complete=False)
        items = order.orderitem_set.all()
    else:
        items = []
        order = {'get_order_total': 0, 'get_order_items': 0}

    context = {'items': items, 'order': order, 'booking': bk}
    return render(request, 'booking/checkout.html', context)


@csrf_exempt
def processOrder(request):
    if request.user.is_authenticated:
        customer = request.user
        order, created = Orders.objects.get_or_create(customer=customer, complete=False)

        order.complete = True
        order.save()

    return JsonResponse('Payment completed', safe=False)


def aboutUs(request):
    return render(request, 'booking/aboutus.html')


@login_required()
def profile(request):
    return render(request, 'booking/profile.html')


@login_required()
def my_restaurant(request):
    rest = models.Restaurants.objects.filter(owner=request.user).first()
    menu = models.Menu.objects.filter(restaurant=rest).first()
    items = models.Items.objects.filter(menu=menu).all().order_by('type')
    bookings = models.Bookings.objects.filter(restaurant=rest)
    orders = models.Orders.objects.filter(booking__in=bookings)
    order_items = models.OrderItem.objects.filter(order__in=orders)
    context = {
        'rest': rest,
        'menu': menu,
        'items': items,
        'bookings': bookings,
        'orders': orders,
        'order_items': order_items
    }
    return render(request, 'booking/my_restaurant.html', context)


@login_required()
def edit_Restaurant(request):
    rest = models.Restaurants.objects.filter(owner=request.user).first()
    rname = request.POST.get('restaurant_name')
    if rname is not "":
        rest.name = rname
    address = request.POST.get('address')
    if address is not "":
        rest.address = address
    total_seats = request.POST.get('total_seats')
    if total_seats is not "":
        rest.total_seats = int(total_seats)
    open_time = request.POST.get('open_time')
    if open_time is not "":
        rest.open_time = datetime.strptime(open_time, '%H:%M').time()
    close_time = request.POST.get('close_time')
    if close_time is not "":
        rest.close_time = datetime.strptime(close_time, '%H:%M').time()
    rest.save()
    messages.info(request, "The restaurant successfully updated!")
    return redirect('my_restaurant')


@login_required()
def addToMenu(request):
    rest = models.Restaurants.objects.filter(owner=request.user).first()
    menu = models.Menu.objects.filter(restaurant=rest).first()
    item_name = request.POST.get('item_name')
    item_price = int(request.POST.get('item_price'))
    item_type = request.POST.get('item_type')
    item_description = request.POST.get('item_description')

    item = Items.objects.create(name=item_name, price=item_price, type=item_type, description=item_description, menu_id=menu.id)
    item.save()
    return redirect('my_restaurant')


@login_required()
def deleteItem(request, item_id):
    item = models.Items.objects.filter(id=item_id)
    item.delete()
    messages.info(request, "Item was successfully deleted!")
    return redirect('my_restaurant')


@login_required()
def editItem(request, item_id):
    item = models.Items.objects.filter(id=item_id).first()
    item_name = request.POST.get('item_name')
    if item_name is not "":
        item.name = item_name
    item_price = request.POST.get('item_price')
    if item_price is not "":
        item.price = int(item_price)
    item_type = request.POST.get('item_type')
    if item_type is not "":
        item.type = item_type
    item_description = request.POST.get('item_description')
    if item_description is not "":
        item.description = item_description
    item.save()
    messages.info(request, "The item successfully updated!")
    return redirect('my_restaurant')
