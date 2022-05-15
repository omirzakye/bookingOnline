from django.contrib import admin
from .models import *

admin.site.register(CustomUser)
admin.site.register(Bookings)
admin.site.register(Orders)
admin.site.register(Items)
admin.site.register(Restaurants)
admin.site.register(Cards)
admin.site.register(Menu)