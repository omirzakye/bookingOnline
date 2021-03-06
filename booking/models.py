from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.models import AbstractUser
from django.db import models


class Cards(models.Model):
    user = models.ForeignKey('CustomUser', models.CASCADE, default=None)
    card_number = models.IntegerField()
    cvc_number = models.IntegerField()
    expire_date = models.DateField()

    class Meta:
        verbose_name = 'Card'
        verbose_name_plural = 'Cards'

    def __str__(self):
        return str(self.card_number)


class CustomUser(AbstractUser):
    phone = models.CharField(max_length=20)


class Items(models.Model):
    menu = models.ForeignKey('Menu', models.CASCADE)
    name = models.CharField(max_length=50)
    price = models.IntegerField()
    type = models.CharField(max_length=50)
    description = models.TextField()
    image = models.ImageField()

    class Meta:
        verbose_name = 'Item'
        verbose_name_plural = 'Items'

    def __str__(self):
        return self.name


class Menu(models.Model):
    restaurant = models.ForeignKey('Restaurants', models.CASCADE)

    class Meta:
        verbose_name = 'Menu'
        verbose_name_plural = 'Menus'


class Restaurants(models.Model):
    owner = models.ForeignKey('CustomUser', models.CASCADE, default=None)
    name = models.CharField(max_length=50)
    address = models.TextField()
    open_time = models.TimeField()
    close_time = models.TimeField()
    instagram = models.TextField()
    photo = models.ImageField()
    total_seats = models.IntegerField()
    busy_seats = models.IntegerField()

    class Meta:
        verbose_name = 'Restaurant'
        verbose_name_plural = 'Restaurants'

    def __str__(self):
        return self.name


class Bookings(models.Model):
    user = models.ForeignKey('CustomUser', models.DO_NOTHING, default=None)
    restaurant = models.ForeignKey('Restaurants', models.CASCADE)
    number_of_people = models.IntegerField()
    reserve_date = models.DateField()
    reserve_time_end = models.TimeField(null=True)
    reserve_time_start = models.TimeField(null=True)
    status = models.BooleanField()
    reserverFname = models.CharField(max_length=50)
    reserverLname = models.CharField(max_length=50)
    phone = models.CharField(max_length=50)
    email = models.EmailField(max_length=50)
    specialRequest = models.TextField()

    class Meta:
        verbose_name = 'Booking'
        verbose_name_plural = 'Bookings'

    def __str__(self):
        return str(self.user) + ' ' + str(self.restaurant)


class Orders(models.Model):
    booking = models.ForeignKey('Bookings', models.CASCADE)
    customer = models.ForeignKey('CustomUser', models.CASCADE, default=None)
    date_ordered = models.DateTimeField(auto_now_add=True)
    complete = models.BooleanField(default=False)

    class Meta:
        verbose_name = 'Order'
        verbose_name_plural = 'Orders'

    def __str__(self):
        return str(self.id)

    @property
    def get_order_total(self):
        orderitems = self.orderitem_set.all()
        total = sum([item.get_total for item in orderitems])
        return total

    @property
    def get_order_items(self):
        orderitems = self.orderitem_set.all()
        total = sum([item.quantity for item in orderitems])
        return total


class OrderItem(models.Model):
    product = models.ForeignKey(Items, on_delete=models.SET_NULL, null=True)
    order = models.ForeignKey(Orders, on_delete=models.SET_NULL, null=True)
    quantity = models.IntegerField(default=0, null=True, blank=True)
    date_added = models.DateTimeField(auto_now_add=True)

    @property
    def get_total(self):
        total = self.product.price * self.quantity
        return total